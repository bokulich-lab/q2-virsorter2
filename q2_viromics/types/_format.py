# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import subprocess

import pandas as pd
from pyhmmer.plan7 import HMMFile
from qiime2.core.exceptions import ValidationError
from qiime2.plugin import model


class ViralScoreFmt(model.TextFileFormat):
    def _validate(self, n_records=None):
        headers = [
            "seqname",
            "dsDNAphage",
            "ssDNA",
            "max_score",
            "max_score_group",
            "length",
            "hallmark",
            "viral",
            "cellular",
        ]

        try:
            df = pd.read_csv(str(self), sep="\t")
        except Exception as e:
            raise ValidationError(f"Error reading file: {e}")

        if list(df.columns) != headers:
            raise ValidationError(
                f"Header mismatch. Expected {headers}, but found {list(df.columns)}."
            )

        for line_number, row in df.iterrows():
            self._validate_fields(line_number + 2, row)

    def _validate_fields(self, line_number, row):
        required_fields = {
            "seqname": str,
            "dsDNAphage": float,
            "ssDNA": float,
            "max_score": float,
            "max_score_group": str,
            "length": int,
            "hallmark": int,
            "viral": float,
            "cellular": float,
        }

        for field, field_type in required_fields.items():
            if field not in row:
                raise ValidationError(f"Line {line_number}: Missing field: {field}")

            value = row[field]
            if pd.isna(value):
                if field in ["seqname", "max_score_group"]:
                    raise ValidationError(
                        f"Line {line_number}: '{field}' field is empty."
                    )
            else:
                self._validate_field_type(value, line_number, field, field_type)

    def _validate_field_type(self, value, line_number, field_name, field_type):
        try:
            field_type(value)
        except ValueError:
            raise ValidationError(
                f"Line {line_number}: '{field_name}' field should be "
                f"{field_type.__name__}, found '{value}'."
            )

    def _validate_(self, level):
        self._validate()


ViralScoreDirFmt = model.SingleFileDirectoryFormat(
    "ViralScoreDirFmt", "final-viral-score.tsv", ViralScoreFmt
)


class ViralBoundaryFmt(model.TextFileFormat):
    def _validate(self, n_records=None):
        headers = [
            "seqname",
            "trim_orf_index_start",
            "trim_orf_index_end",
            "trim_bp_start",
            "trim_bp_end",
            "trim_pr",
            "trim_pr_max",
            "prox_orf_index_start",
            "prox_orf_index_end",
            "prox_bp_start",
            "prox_bp_end",
            "prox_pr",
            "prox_pr_max",
            "partial",
            "full_orf_index_start",
            "full_orf_index_end",
            "full_bp_start",
            "full_bp_end",
            "pr_full",
            "arc",
            "bac",
            "euk",
            "vir",
            "mix",
            "unaligned",
            "hallmark_cnt",
            "group",
            "shape",
            "seqname_new",
            "final_max_score",
            "final_max_score_group",
        ]

        try:
            df = pd.read_csv(str(self), sep="\t")
        except Exception as e:
            raise ValidationError(f"Error reading file: {e}")

        if df.empty:
            raise ValidationError("File is empty.")

        if list(df.columns) != headers:
            raise ValidationError(
                f"Header mismatch. Expected {headers}, but found {list(df.columns)}."
            )

        for line_number, row in df.iterrows():
            self._validate_fields(line_number + 2, row)

    def _validate_fields(self, line_number, fields):
        required_fields = ["seqname", "seqname_new", "final_max_score_group"]
        int_fields = [
            "trim_orf_index_start",
            "trim_orf_index_end",
            "trim_bp_start",
            "trim_bp_end",
            "prox_orf_index_start",
            "prox_orf_index_end",
            "prox_bp_start",
            "prox_bp_end",
            "partial",
            "full_orf_index_start",
            "full_orf_index_end",
            "full_bp_start",
            "full_bp_end",
            "hallmark_cnt",
        ]
        float_fields = [
            "trim_pr",
            "trim_pr_max",
            "prox_pr",
            "prox_pr_max",
            "pr_full",
            "arc",
            "bac",
            "euk",
            "vir",
            "mix",
            "unaligned",
            "final_max_score",
        ]

        for field in required_fields:
            if pd.isna(fields[field]):
                raise ValidationError(f"Line {line_number}: '{field}' field is empty.")

        for field in int_fields:
            self._validate_numeric_field(fields[field], line_number, field, int)

        for field in float_fields:
            self._validate_numeric_field(fields[field], line_number, field, float)

    def _validate_numeric_field(self, value, line_number, field_name, field_type):
        if pd.notna(value):
            try:
                field_type(value)
            except ValueError:
                raise ValidationError(
                    f"Line {line_number}: '{field_name}' field should be a "
                    f"{field_type.__name__}, found '{value}'."
                )

    def _validate_(self, level):
        self._validate()


ViralBoundaryDirFmt = model.SingleFileDirectoryFormat(
    "ViralBoundaryDirFmt", "final-viral-boundary.tsv", ViralBoundaryFmt
)


# Format for validating general TSV files
class GeneralTSVFormat(model.TextFileFormat):
    def _validate_(self, level):
        try:
            # Read the TSV file into a DataFrame
            df = pd.read_csv(str(self), sep="\t", dtype=str, keep_default_na=False)

            # Ensure that the file is not empty
            if df.empty:
                raise ValidationError("The file is empty.")

            # Check for empty fields
            if (df == "").any().any():
                first_empty = df.eq("").stack().idxmax()
                line_number = first_empty[0] + 1
                column_number = first_empty[1] + 1
                raise ValidationError(
                    f"Line {line_number}: Field {column_number} is empty."
                )

        except pd.errors.ParserError as e:
            raise ValidationError(f"File could not be parsed as TSV: {e}")
        except Exception as e:
            raise ValidationError(f"Validation error: {e}")


# Format for validating RBS catetory notes files
class RbsCatetoryNotesFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        try:
            # Read the file, skipping lines that start with '#'
            df = pd.read_csv(
                str(self),
                sep="\t",
                header=None,
                comment="#",
                dtype=str,
                keep_default_na=False,
            )

            # Ensure that the file is not empty and has exactly 2 fields
            if df.empty:
                raise ValidationError("The file is empty.")
            if df.shape[1] != 2:
                raise ValidationError(f"Expected 2 fields, but found {df.shape[1]}.")

            # Check for non-empty RBS categories and notes
            if (df == "").any().any():
                first_empty = df.eq("").stack().idxmax()
                line_number = first_empty[0] + 1
                column_name = ["RBS category", "Note"][first_empty[1]]
                raise ValidationError(f"Line {line_number}: {column_name} is empty.")

        except pd.errors.ParserError as e:
            raise ValidationError(f"File could not be parsed: {e}")
        except Exception as e:
            raise ValidationError(f"Validation error: {e}")

    def _validate_(self, level):
        self._validate()


# Format for validating RBS catetory files
class RbsCatetoryFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        try:
            # Read the file, skipping lines that start with '#'
            df = pd.read_csv(
                str(self),
                sep="\t",
                header=None,
                comment="#",
                dtype=str,
                keep_default_na=False,
            )

            # Ensure that the file is not empty and has exactly 2 fields
            if df.empty:
                raise ValidationError("The file is empty.")
            if df.shape[1] != 2:
                raise ValidationError(f"Expected 2 fields, but found {df.shape[1]}.")

            # Check for non-empty RBS and categories
            if (df == "").any().any():
                first_empty = df.eq("").stack().idxmax()
                line_number = first_empty[0] + 1
                column_name = ["RBS", "category"][first_empty[1]]
                raise ValidationError(f"Line {line_number}: {column_name} is empty.")

        except pd.errors.ParserError as e:
            raise ValidationError(f"File could not be parsed: {e}")
        except Exception as e:
            raise ValidationError(f"Validation error: {e}")

    def _validate_(self, level):
        self._validate()


# Format for validating hallmark gene list files
class HallmarkGeneListFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        try:
            # Read the file into a DataFrame
            df = pd.read_csv(
                str(self), sep="\t", header=None, dtype=str, keep_default_na=False
            )

            # Ensure that the file is not empty and has exactly 3 fields
            if df.empty:
                raise ValidationError("The file is empty.")
            if df.shape[1] != 3:
                raise ValidationError(f"Expected 3 fields, but found {df.shape[1]}.")

            # Check for non-empty gene names, descriptions, and properties
            if (df == "").any().any():
                empty_field = df.eq("").idxmax(axis=1).max()
                line_number = df.eq("").idxmax(axis=1)[empty_field] + 1
                column_name = ["Gene name", "Gene description", "Gene property"][
                    empty_field
                ]
                raise ValidationError(f"Line {line_number}: {column_name} is empty.")

        except pd.errors.ParserError as e:
            raise ValidationError(f"File could not be parsed: {e}")
        except Exception as e:
            raise ValidationError(f"Validation error: {e}")

    def _validate_(self, level):
        self._validate()


class GeneralBinaryFileFormat(model.BinaryFileFormat):
    def _validate_(self, level):
        pass


# Format for validating HMM profiles files
class HMMFormat(model.TextFileFormat):
    def _validate_(self, level: str):
        tolerance = 0.0001
        with HMMFile(str(self)) as hmm_file:
            hmm = hmm_file.read()

            try:
                hmm.validate(tolerance=tolerance)
            except subprocess.CalledProcessError as e:
                raise ValidationError(
                    f"An error was encountered while validating hmm file, "
                    f"(return code {e.returncode})."
                )


# Directory format for the Virsorter2 Database
class Virsorter2DbDirFmt(model.DirectoryFormat):
    hmm_files = model.FileCollection(r"hmm/.+/.+\.hmm$", format=HMMFormat)
    tsv_file = model.FileCollection(
        r"hmm/.+/.+\.tsv$", format=GeneralTSVFormat, optional=True
    )

    hallmark_gene_list = model.FileCollection(
        r"group/.+/.+\.list$", format=HallmarkGeneListFormat
    )
    model_file = model.FileCollection(
        r"group/.+/model$", format=GeneralBinaryFileFormat, optional=True
    )
    db_files = model.FileCollection(
        r"group/.+/.+\.db$", format=GeneralBinaryFileFormat, optional=True
    )
    rbs_catetory_notes = model.File(
        r"rbs/rbs-catetory-notes.tsv$", format=RbsCatetoryNotesFormat, optional=True
    )
    rbs_catetory = model.File(
        r"rbs/rbs-catetory.tsv$", format=RbsCatetoryFormat, optional=True
    )
    done_all_setup = model.File(r"Done_all_setup$", format=GeneralBinaryFileFormat)

    @hmm_files.set_path_maker
    def hmm_files_path_maker(self, sample_id):
        return "hmm/{}/{}.hmm".format(sample_id[0], sample_id[1])

    @tsv_file.set_path_maker
    def tsv_file_path_maker(self, sample_id):
        return "hmm/{}/{}.tsv".format(sample_id[0], sample_id[1])

    @hallmark_gene_list.set_path_maker
    def hallmark_gene_list_path_maker(self, sample_id):
        return "group/{}/{}.list".format(sample_id[0], sample_id[1])

    @model_file.set_path_maker
    def model_file_path_maker(self, sample_id):
        return "group/{}/model".format(sample_id[0])

    @db_files.set_path_maker
    def db_files_path_maker(self, sample_id):
        return "group/{}/{}.db".format(sample_id[0], sample_id[1])

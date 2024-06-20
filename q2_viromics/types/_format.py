# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.core.exceptions import ValidationError
from qiime2.plugin import model


# Format for validating general TSV files
class GeneralTSVFormat(model.TextFileFormat):
    def _validate_(self, level):
        with open(str(self), "r") as file:
            line_number = 0
            num_fields = None
            for line in file:
                line_number += 1
                fields = line.strip().split("\t")

                # Determine the number of fields from the first line
                if num_fields is None:
                    num_fields = len(fields)
                elif len(fields) != num_fields:
                    raise ValidationError(
                        f"Line {line_number}: Expected {num_fields} fields, "
                        f"but found {len(fields)}."
                    )

                # Ensure no field is empty
                for idx, field in enumerate(fields):
                    if field == "":
                        raise ValidationError(
                            f"Line {line_number}: Field {idx + 1} is empty."
                        )


# Format for validating RBS catetory notes files
class RbsCatetoryNotesFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        with open(str(self), "r") as file:
            line_number = 0
            for line in file:
                line_number += 1
                # Skip header
                if line.startswith("#"):
                    continue

                fields = line.strip().split("\t")

                # Check for exactly 2 fields
                if len(fields) != 2:
                    raise ValidationError(
                        f"Line {line_number}: Expected 2 fields, "
                        f"but found {len(fields)}."
                    )

                # Check that RBS catetories and notes are non-empty
                rbs_catetory = fields[0]
                note = fields[1]
                if not rbs_catetory:
                    raise ValidationError(
                        f"Line {line_number}: RBS" " catetory is empty."
                    )
                if not note:
                    raise ValidationError(f"Line {line_number}: Note is empty.")

    def _validate_(self, level):
        self._validate()


# Format for validating RBS catetory files
class RbsCatetoryFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        with open(str(self), "r") as file:
            line_number = 0
            for line in file:
                line_number += 1
                # Skip header
                if line.startswith("#"):
                    continue

                fields = line.strip().split("\t")

                # Check for exactly 2 fields
                if len(fields) != 2:
                    raise ValidationError(
                        f"Line {line_number}: Expected 2 fields, "
                        f"but found {len(fields)}."
                    )

                # Check that RBS and catetories are non-empty
                rbs = fields[0]
                catetory = fields[1]
                if not rbs:
                    raise ValidationError(f"Line {line_number}: RBS is empty.")
                if not catetory:
                    raise ValidationError(f"Line {line_number}: " "catetory is empty.")

    def _validate_(self, level):
        self._validate()


# Format for validating hallmark gene list files
class HallmarkGeneListFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        with open(str(self), "r") as file:
            line_number = 0
            for line in file:
                line_number += 1
                fields = line.strip().split("\t")

                # Check for exactly 3 fields
                if len(fields) != 3:
                    raise ValidationError(
                        f"Line {line_number}: Expected 3 fields, "
                        f"but found {len(fields)}."
                    )

                # Further validation could be added here if necessary, for example:
                # Check that gene names are non-empty
                gene_name = fields[0]
                if not gene_name:
                    raise ValidationError(f"Line {line_number}: Gene " "name is empty.")

                # Check that gene descriptions are non-empty
                gene_description = fields[1]
                if not gene_description:
                    raise ValidationError(
                        f"Line {line_number}: Gene description is empty."
                    )

                # Validate specific conditions for the third column if needed
                # gene_property = fields[2]
                # Add any specific validation rules for the third column here

    def _validate_(self, level):
        self._validate()


class GeneralBinaryFileFormat(model.BinaryFileFormat):
    def _validate_(self, level):
        pass


# Format for validating HMM profiles files
class HMMFormat(model.TextFileFormat):
    def _validate_(self, level):
        with open(str(self), "r") as file:
            lines = file.readlines()
            mandatory_fields, optional_fields = self._read_header_tags(lines)
            self._validate_mandatory_fields(mandatory_fields)
            self._validate_optional_fields(optional_fields)

    def _read_header_tags(self, lines):
        # Define mandatory and optional fields for HMM files
        mandatory_fields = {
            "HMMER3": None,
            "NAME": None,
            "LENG": None,
            "ALPH": None,
            "HMM": None,
        }

        optional_fields = {
            "ACC": None,
            "DESC": None,
            "RF": None,
            "MM": None,
            "CONS": None,
            "CS": None,
            "MAP": None,
            "DATE": None,
            "MAXL": None,
            "COM": None,
            "NSEQ": None,
            "EFFN": None,
            "CKSUM": None,
            "BM": None,
            "SM": None,
            "GA": None,
            "TC": None,
            "NC": None,
            "STATS": None,
            "COMPO": None,
        }

        for line in lines:
            if line.strip() == "":
                continue
            parts = line.split(maxsplit=1)
            field_name = parts[0]

            if field_name.startswith("HMMER3"):
                if mandatory_fields["HMMER3"]:
                    raise ValidationError(f"Duplicate field {field_name} HMMER3.")
                mandatory_fields["HMMER3"] = parts[0]

            elif field_name in mandatory_fields:
                if mandatory_fields[field_name]:
                    raise ValidationError(f"Duplicate field {field_name} found.")
                mandatory_fields[field_name] = (
                    str(parts[1].strip()) if len(parts) > 1 else ""
                )

                if field_name == "HMM":
                    mandatory_fields["HMM"] = (
                        str(parts[1].strip()) if len(parts) > 1 else ""
                    )
                    break

            elif field_name in optional_fields:
                if optional_fields[field_name] and field_name != "STATS":
                    raise ValidationError(f"Duplicate field {field_name} found.")
                optional_fields[field_name] = parts[1].strip() if len(parts) > 1 else ""
            else:
                raise ValidationError(f"Unexpected field {field_name} found.")

        return mandatory_fields, optional_fields

    # Validate the mandatory fields for the HMM format
    def _validate_mandatory_fields(self, mandatory_fields):
        # Check if all mandatory fields are present
        for field_name, value in mandatory_fields.items():
            if value is None:
                raise ValidationError(f"Mandatory field {field_name} is missing.")

        # Validate the HMM block exists
        if not mandatory_fields["HMM"]:
            raise ValidationError("HMM block is missing.")

        if int(mandatory_fields["LENG"]) <= 0:
            raise ValidationError("LENG field should be a positive nonzero integer.")

        if mandatory_fields["ALPH"] not in [
            "amino",
            "dna",
            "rna",
            "coins",
            "dice",
            "custom",
        ]:
            raise ValidationError(
                "ALPH field should be 'amino', 'DNA', 'RNA', 'coins', "
                "'dice' or 'custom'."
            )

        # Validate NAME field
        if (
            not mandatory_fields["NAME"]
            or " " in mandatory_fields["NAME"]
            or "\t" in mandatory_fields["NAME"]
        ):
            raise ValidationError(
                "NAME field must be a single word containing no spaces or tabs."
            )

    # Validate the optional fields for the HMM format
    def _validate_optional_fields(self, optional_fields):
        for field in ["RF", "MM", "CONS", "CS", "MAP"]:
            if optional_fields[field] and optional_fields[field] not in [
                "yes",
                "no",
            ]:
                raise ValidationError(f"{field} field should be 'yes' or 'no'.")

        if optional_fields["NSEQ"]:
            try:
                if int(optional_fields["NSEQ"]) <= 0:
                    raise ValidationError(
                        "NSEQ field should be a nonzero positive integer."
                    )
            except ValueError:
                raise ValidationError(
                    "NSEQ field should be a nonzero positive integer."
                )

        # Validate EFFN field
        if optional_fields["EFFN"]:
            try:
                if float(optional_fields["EFFN"]) <= 0:
                    raise ValidationError(
                        "EFFN field should be a nonzero positive real number."
                    )
            except ValueError:
                raise ValidationError(
                    "EFFN field should be a nonzero positive real number."
                )

        # Validate CKSUM field
        if optional_fields["CKSUM"]:
            try:
                if int(optional_fields["CKSUM"]) < 0:
                    raise ValidationError(
                        "CKSUM field should be a nonnegative unsigned 32-bit integer."
                    )
            except ValueError:
                raise ValidationError(
                    "CKSUM field should be a nonnegative unsigned 32-bit integer."
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

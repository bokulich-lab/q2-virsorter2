# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import shutil
import subprocess
import tempfile

import pandas as pd
from q2_types.feature_data import DNAFASTAFormat

from q2_viromics._utils import run_command
from q2_viromics.types._format import Virsorter2DbDirFmt


# Create the command to fetch the Virsorter2 database
def vs2_run_execution(tmp, sequences, database, n_jobs):
    cmd = [
        "virsorter",
        "run",
        "-w",
        str(tmp),
        "-d",
        str(database.path),
        "-i",
        str(sequences.path),
        "-j",
        str(n_jobs),
        "--use-conda-off",
    ]

    try:
        run_command(cmd)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running virsorter2 run, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


def _virsorter2_analysis(
    sequences: DNAFASTAFormat,
    database: Virsorter2DbDirFmt,
    n_jobs: int = 10,
) -> (DNAFASTAFormat, pd.DataFrame, pd.DataFrame):

    viral_sequences = DNAFASTAFormat()

    with tempfile.TemporaryDirectory() as tmp:
        # Execute the "virsorter2 run" command
        vs2_run_execution(tmp, sequences, database, n_jobs)

        # Copy the combined viral sequences file
        shutil.copy(
            os.path.join(tmp, "final-viral-combined.fa"),
            os.path.join(str(viral_sequences)),
        )

        # Read the viral score file into a DataFrame
        viral_score_df = pd.read_csv(
            os.path.join(tmp, "final-viral-score.tsv"), sep="\t"
        )

        # Read the viral boundary file into a DataFrame
        viral_boundary_df = pd.read_csv(
            os.path.join(tmp, "final-viral-boundary.tsv"), sep="\t"
        )

    return (viral_sequences, viral_score_df, viral_boundary_df)


def virsorter2_run(
    ctx,
    sequences,
    database,
    n_jobs=10,
):
    vs2_analysis = ctx.get_action("viromics", "_virsorter2_analysis")
    (viral_sequences, viral_score_table, viral_boundary_table) = vs2_analysis(
        sequences=sequences, database=database, n_jobs=n_jobs
    )

    return viral_sequences, viral_score_table, viral_boundary_table

# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import subprocess
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from q2_viromics.virsorter2_run import (
    _virsorter2_analysis,
    virsorter2_run,
    vs2_run_execution,
)


class TestVirsorter2Analysis(unittest.TestCase):
    @patch("q2_viromics.virsorter2_run.run_command")
    @patch("q2_viromics.virsorter2_run.DNAFASTAFormat")
    @patch("q2_viromics.virsorter2_run.Virsorter2DbDirFmt")
    def test_vs2_run_execution_success(
        self, mock_Virsorter2DbDirFmt, mock_DNAFASTAFormat, mock_run_command
    ):
        # Mock the paths
        mock_tmp = "/fake/tmp"
        mock_sequences = MagicMock()
        mock_sequences.path = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"

        # Call the function
        vs2_run_execution(mock_tmp, mock_sequences, mock_database, n_jobs=5)

        # Expected command
        expected_cmd = [
            "virsorter",
            "run",
            "-w",
            mock_tmp,
            "-d",
            mock_database.path,
            "-i",
            mock_sequences.path,
            "-j",
            "5",
            "--use-conda-off",
        ]

        # Assert the command was called
        mock_run_command.assert_called_once_with(expected_cmd)

    @patch(
        "q2_viromics.virsorter2_run.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    def test_vs2_run_execution_failure(self, mock_run_command):
        # Mock the paths
        mock_tmp = "/fake/tmp"
        mock_sequences = MagicMock()
        mock_sequences.path = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"

        # Call the function and assert it raises an Exception
        with self.assertRaises(Exception) as context:
            vs2_run_execution(mock_tmp, mock_sequences, mock_database, n_jobs=5)

        self.assertTrue(
            "An error was encountered while running virsorter2 run"
            in str(context.exception)
        )

    @patch("q2_viromics.virsorter2_run.vs2_run_execution")
    @patch("q2_viromics.virsorter2_run.DNAFASTAFormat")
    @patch("q2_viromics.virsorter2_run.pd.read_csv")
    @patch("shutil.copy")
    @patch("tempfile.TemporaryDirectory")
    def test_virsorter2_analysis_success(
        self,
        mock_tempdir,
        mock_shutil_copy,
        mock_read_csv,
        mock_DNAFASTAFormat,
        mock_vs2_run_execution,
    ):
        # Mock the context managers
        mock_tempdir.return_value.__enter__.return_value = "/fake/tmp"

        # Mock the data frames
        mock_viral_score_df = pd.DataFrame({"mock": ["data"]})
        mock_viral_boundary_df = pd.DataFrame({"mock": ["data"]})
        mock_read_csv.side_effect = [mock_viral_score_df, mock_viral_boundary_df]

        # Mock the sequences and database
        mock_sequences = MagicMock()
        mock_sequences.path = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"

        # Call the function
        result = _virsorter2_analysis(mock_sequences, mock_database, n_jobs=5)

        # Assertions
        mock_vs2_run_execution.assert_called_once_with(
            "/fake/tmp", mock_sequences, mock_database, 5
        )
        mock_shutil_copy.assert_called_once_with(
            "/fake/tmp/final-viral-combined.fa", str(result[0])
        )
        mock_read_csv.assert_any_call("/fake/tmp/final-viral-score.tsv", sep="\t")
        mock_read_csv.assert_any_call("/fake/tmp/final-viral-boundary.tsv", sep="\t")

        self.assertEqual(result[1].equals(mock_viral_score_df), True)
        self.assertEqual(result[2].equals(mock_viral_boundary_df), True)

    @patch("q2_viromics.virsorter2_run._virsorter2_analysis")
    @patch("q2_viromics.virsorter2_run.Virsorter2DbDirFmt")
    @patch("q2_viromics.virsorter2_run.DNAFASTAFormat")
    def test_virsorter2_run(
        self, mock_DNAFASTAFormat, mock_Virsorter2DbDirFmt, mock_virsorter2_analysis
    ):
        # Mock the context
        mock_ctx = MagicMock()
        mock_ctx.get_action.return_value = mock_virsorter2_analysis

        # Mock the analysis result
        mock_viral_sequences = MagicMock()
        mock_viral_score_df = pd.DataFrame({"mock": ["data"]})
        mock_viral_boundary_df = pd.DataFrame({"mock": ["data"]})
        mock_virsorter2_analysis.return_value = (
            mock_viral_sequences,
            mock_viral_score_df,
            mock_viral_boundary_df,
        )

        # Mock the sequences and database
        mock_sequences = MagicMock()
        mock_sequences.path = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"

        # Call the function
        result = virsorter2_run(mock_ctx, mock_sequences, mock_database, n_jobs=5)

        # Assertions
        mock_virsorter2_analysis.assert_called_once_with(
            sequences=mock_sequences, database=mock_database, n_jobs=5
        )
        self.assertEqual(result[0], mock_viral_sequences)
        self.assertTrue(result[1].equals(mock_viral_score_df))
        self.assertTrue(result[2].equals(mock_viral_boundary_df))


if __name__ == "__main__":
    unittest.main()

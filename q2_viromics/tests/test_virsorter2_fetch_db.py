# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import subprocess
import unittest
from unittest.mock import MagicMock, patch

from q2_viromics.virsorter2_fetch_db import virsorter2_fetch_db, vs2_setup


class TestVirsorter2FetchDb(unittest.TestCase):
    @patch("q2_viromics.virsorter2_fetch_db.run_command")
    @patch("q2_viromics.virsorter2_fetch_db.Virsorter2DbDirFmt")
    def test_virsorter2_fetch_db_success(
        self, mock_Virsorter2DbDirFmt, mock_run_command
    ):
        # Mock the Virsorter2DbDirFmt instance
        mock_database = MagicMock()
        mock_Virsorter2DbDirFmt.return_value = mock_database

        # Call the function
        result = virsorter2_fetch_db(n_jobs=5)

        # Check if vs2_setup was called correctly
        expected_cmd = [
            "virsorter",
            "setup",
            "-d",
            str(mock_database),
            "-s",
            "-j",
            "5",
        ]
        mock_run_command.assert_called_once_with(expected_cmd)

        # Check if directories are deleted
        self.assertFalse(os.path.exists(".snakemake"))
        self.assertFalse(os.path.exists("conda_envs"))

        # Check the return value
        self.assertEqual(result, mock_database)

    @patch(
        "q2_viromics.virsorter2_fetch_db.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    @patch("q2_viromics.virsorter2_fetch_db.Virsorter2DbDirFmt")
    def test_virsorter2_fetch_db_failure(
        self, mock_Virsorter2DbDirFmt, mock_run_command
    ):
        # Mock the Virsorter2DbDirFmt instance
        mock_database = MagicMock()
        mock_Virsorter2DbDirFmt.return_value = mock_database

        # Call the function and assert it raises an Exception
        with self.assertRaises(Exception) as context:
            virsorter2_fetch_db(n_jobs=5)

        self.assertTrue(
            "An error was encountered while running virsorter2 setup"
            in str(context.exception)
        )

    @patch("q2_viromics.virsorter2_fetch_db.run_command")
    def test_vs2_setup_success(self, mock_run_command):
        # Mock the database path
        mock_database = MagicMock()
        mock_database.path = "/fake/path"

        # Call the function
        vs2_setup(mock_database, n_jobs=5)

        # Expected command
        expected_cmd = [
            "virsorter",
            "setup",
            "-d",
            str(mock_database),
            "-s",
            "-j",
            "5",
        ]

        # Assert the command was called
        mock_run_command.assert_called_once_with(expected_cmd)

    @patch(
        "q2_viromics.virsorter2_fetch_db.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    def test_vs2_setup_failure(self, mock_run_command):
        # Mock the database path
        mock_database = MagicMock()
        mock_database.path = "/fake/path"

        # Call the function and assert it raises an Exception
        with self.assertRaises(Exception) as context:
            vs2_setup(mock_database, n_jobs=5)

        self.assertTrue(
            "An error was encountered while running virsorter2 setup"
            in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()

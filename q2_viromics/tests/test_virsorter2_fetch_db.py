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

from q2_viromics.virsorter2_fetch_db import (  # Adjust import as necessary
    create_fetch_db_cmd,
    delete_directory,
    virsorter2_fetch_db,
)


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

        # Check if create_fetch_db_cmd was called correctly
        expected_cmd = create_fetch_db_cmd(mock_database, 5)
        mock_run_command.assert_called_once_with(expected_cmd)

        # Check if directories are deleted
        mock_database_path = str(mock_database.path)
        expected_snakemake_path = os.path.join(mock_database_path, ".snakemake")
        expected_conda_envs_path = os.path.join(mock_database_path, "conda_envs")
        self.assertFalse(os.path.exists(expected_snakemake_path))
        self.assertFalse(os.path.exists(expected_conda_envs_path))

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

    @patch("q2_viromics.virsorter2_fetch_db.os.path.exists", return_value=True)
    @patch("q2_viromics.virsorter2_fetch_db.shutil.rmtree")
    def test_delete_directory(self, mock_rmtree, mock_exists):
        # Call the function
        delete_directory("/fake/path")

        # Check if shutil.rmtree was called
        mock_rmtree.assert_called_once_with("/fake/path")

    @patch("q2_viromics.virsorter2_fetch_db.os.path.exists", return_value=False)
    @patch("q2_viromics.virsorter2_fetch_db.shutil.rmtree")
    def test_delete_directory_not_exists(self, mock_rmtree, mock_exists):
        # Call the function
        delete_directory("/fake/path")

        # Check if shutil.rmtree was not called
        mock_rmtree.assert_not_called()

    @patch("q2_viromics.virsorter2_fetch_db.Virsorter2DbDirFmt")
    def test_create_fetch_db_cmd(self, mock_Virsorter2DbDirFmt):
        # Mock the Virsorter2DbDirFmt instance
        mock_database = MagicMock()
        mock_database.path = "/fake/path"

        # Call the function
        result = create_fetch_db_cmd(mock_database, n_jobs=5)

        # Expected command
        expected_cmd = ["virsorter", "setup", "-d", "/fake/path", "-s", "-j", "5"]

        # Assert the result matches the expected command
        self.assertEqual(result, expected_cmd)


if __name__ == "__main__":
    unittest.main()

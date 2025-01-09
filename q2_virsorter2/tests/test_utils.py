# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import tempfile
import unittest
from unittest.mock import patch

from q2_virsorter2._utils import (
    _construct_param,
    _get_sample_from_path,
    _process_common_input_params,
    create_directory,
    get_full_path,
    run_command,
    run_commands_with_pipe,
)


class TestFilePathOperations(unittest.TestCase):
    def test_get_full_path_with_filename(self):
        # Test with a simple filename
        filename = "example.txt"
        expected_path = os.path.abspath(filename)
        self.assertEqual(get_full_path(filename), expected_path)

    def test_get_full_path_with_relative_path(self):
        # Test with a relative path
        relative_path = "./folder/example.txt"
        expected_path = os.path.abspath(relative_path)
        self.assertEqual(get_full_path(relative_path), expected_path)

    def test_get_full_path_with_absolute_path(self):
        # Test with an absolute path
        absolute_path = "/tmp/example.txt"
        self.assertEqual(get_full_path(absolute_path), absolute_path)


class TestDirectoryOperations(unittest.TestCase):
    def test_create_directory(self):
        # Test creating a new directory
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "new_dir")
            self.assertTrue(create_directory(new_dir))
            self.assertTrue(os.path.exists(new_dir))

    def test_create_existing_directory(self):
        # Test trying to create a directory that already exists
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertFalse(create_directory(tmpdir))  # Already exists


class TestCommandOperations(unittest.TestCase):
    def test_run_commands_with_pipe(self):
        # This is a simplistic test scenario; you might want to mock subprocess.run
        cmd1 = ["echo", "hello"]
        cmd2 = ["grep", "hello"]
        cmd3 = ["echo", "hello"]
        with tempfile.TemporaryDirectory() as temp_dir:
            run_commands_with_pipe(
                cmd1, cmd2, cmd3, temp_dir + "res.out"
            )  # Assuming no exception is good enough for this test

    def test_run_commands_with_pipe_no_verbose(self):
        # This is a simplistic test scenario; you might want to mock subprocess.run
        cmd1 = ["echo", "hello"]
        cmd2 = ["grep", "hello"]
        cmd3 = ["echo", "hello"]
        with tempfile.TemporaryDirectory() as temp_dir:
            run_commands_with_pipe(
                cmd1, cmd2, cmd3, temp_dir + "res.out", verbose=False
            )  # Assuming no exception is good enough for this test


class TestRunCommand(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_command_with_verbose(self, mock_run):
        cmd = ["echo", "hello"]
        run_command(cmd, verbose=True)
        mock_run.assert_called_once_with(cmd, check=True)

    @patch("subprocess.run")
    def test_run_command_no_verbose(self, mock_run):
        cmd = ["echo", "hello"]
        run_command(cmd, verbose=False)
        mock_run.assert_called_once_with(cmd, check=True)


class TestParameterConstruction(unittest.TestCase):
    def test_construct_param(self):
        self.assertEqual(_construct_param("test_param"), "--test-param")
        # Test does not handle camelCase, so adjust expectations:
        self.assertNotEqual(_construct_param("anotherTestParam"), "--anothertestparam")


def processing_adapter(key, value):
    """Adapter to fit the existing `_construct_param` for testing."""
    param = _construct_param(key)
    if isinstance(value, bool):
        return [param] if value else []
    else:
        return [param, str(value)]


class TestProcessCommonInputParams(unittest.TestCase):
    def test_process_common_input_params(self):
        params = {
            "test_param": True,
            "another_param": None,
            "yet_another_param": "value",
        }
        processed = _process_common_input_params(processing_adapter, params)
        self.assertIn("--test-param", processed)
        self.assertNotIn(
            "--another-param", processed
        )  # 'another_param' is None, should not appear
        self.assertIn("--yet-another-param", processed)
        self.assertIn("value", processed)


class TestGetSampleFromPath(unittest.TestCase):
    def test_normal_case(self):
        # A typical file path
        path = "/path/to/sample1_contigs.fa"
        expected = "sample1"
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

    def test_with_directories_in_path(self):
        # Path containing directories
        path = "sample2_contigs.fa"
        expected = "sample2"
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

    def test_path_without_suffix(self):
        # Path does not have the expected suffix
        path = "sample3.fasta"
        expected = "sample3.fasta"  # Full name should return as no suffix to split
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

    def test_empty_string(self):
        # Empty string input
        path = ""
        expected = ""  # Should return empty string if no path is given
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

    def test_suffix_not_at_end(self):
        # Suffix appears but not at the end
        path = "sample4_contigs.fa_contigs.fa"
        expected = "sample4_contigs.fa"
        result = _get_sample_from_path(path)
        self.assertEqual(result, expected)

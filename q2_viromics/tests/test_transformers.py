# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import unittest

import pandas as pd
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.types._format import ViralBoundaryDirFmt, ViralScoreDirFmt


class TestTransformers(TestPluginBase):
    package = "q2_viromics.tests"

    def setUp(self):
        super().setUp()

    def tearDown(self):
        # Clean up temporary directory
        self.temp_dir.cleanup()

    def test_dataframe_to_viral_score_dir_format(self):
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        transformer = self.get_transformer(pd.DataFrame, ViralScoreDirFmt)
        obs = transformer(df)
        self.assertIsInstance(obs, ViralScoreDirFmt)
        transformed_df = pd.read_csv(
            os.path.join(str(obs), "final-viral-score.tsv"), sep="\t"
        )
        pd.testing.assert_frame_equal(df, transformed_df)

    def test_viral_score_dir_format_to_dataframe(self):
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        ff = ViralScoreDirFmt()
        df.to_csv(os.path.join(str(ff), "final-viral-score.tsv"), sep="\t", index=False)
        transformer = self.get_transformer(ViralScoreDirFmt, pd.DataFrame)
        obs = transformer(ff)
        self.assertIsInstance(obs, pd.DataFrame)
        pd.testing.assert_frame_equal(df, obs)

    def test_dataframe_to_viral_boundary_dir_format(self):
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        transformer = self.get_transformer(pd.DataFrame, ViralBoundaryDirFmt)
        obs = transformer(df)
        self.assertIsInstance(obs, ViralBoundaryDirFmt)
        transformed_df = pd.read_csv(
            os.path.join(str(obs), "final-viral-boundary.tsv"), sep="\t"
        )
        pd.testing.assert_frame_equal(df, transformed_df)

    def test_viral_boundary_dir_format_to_dataframe(self):
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        ff = ViralBoundaryDirFmt()
        df.to_csv(
            os.path.join(str(ff), "final-viral-boundary.tsv"), sep="\t", index=False
        )
        transformer = self.get_transformer(ViralBoundaryDirFmt, pd.DataFrame)
        obs = transformer(ff)
        self.assertIsInstance(obs, pd.DataFrame)
        pd.testing.assert_frame_equal(df, obs)


if __name__ == "__main__":
    unittest.main()

# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import pandas as pd

from q2_viromics.types._format import ViralBoundaryDirFmt, ViralScoreDirFmt

from ..plugin_setup import plugin


@plugin.register_transformer
def _1(data: pd.DataFrame) -> ViralScoreDirFmt:
    ff = ViralScoreDirFmt()
    data.to_csv(os.path.join(str(ff), "final-viral-score.tsv"), sep="\t", index=False)
    return ff


@plugin.register_transformer
def _2(data: ViralScoreDirFmt) -> pd.DataFrame:
    file = pd.read_csv(os.path.join(str(data), "final-viral-score.tsv"), sep="\t")
    return file


@plugin.register_transformer
def _3(data: pd.DataFrame) -> ViralBoundaryDirFmt:
    ff = ViralBoundaryDirFmt()
    data.to_csv(
        os.path.join(str(ff), "final-viral-boundary.tsv"), sep="\t", index=False
    )
    return ff


@plugin.register_transformer
def _4(data: ViralBoundaryDirFmt) -> pd.DataFrame:
    file = pd.read_csv(os.path.join(str(data), "final-viral-boundary.tsv"), sep="\t")
    return file

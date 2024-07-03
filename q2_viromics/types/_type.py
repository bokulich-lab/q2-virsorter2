# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.feature_data import FeatureData
from qiime2.plugin import SemanticType

Virsorter2Db = SemanticType("Virsorter2Db")
ViralScore = SemanticType("ViralScore", variant_of=FeatureData.field["type"])
ViralBoundary = SemanticType("ViralBoundary", variant_of=FeatureData.field["type"])

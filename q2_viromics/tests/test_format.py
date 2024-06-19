# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.types._format import (
    GeneralFileFormat,
    GeneralTSVFormat,
    HallmarkGeneListFormat,
    RbsCatetoryFormat,
    RbsCatetoryNotesFormat,
    Virsorter2DbDirFmt,
)


class TestVirsorter2DbFormats(TestPluginBase):
    package = "q2_viromics.tests"

    def test_Virsorter2Db_GeneralTSVFormat(self):
        filepath = self.get_data_path("type/database/hmm/pfam/Pfam-A.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        format.validate()

    def test_Virsorter2Db_RbsCategoryNotesFormat(self):
        filepath = self.get_data_path("type/database/rbs/rbs-catetory-notes.tsv")
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        format.validate()

    def test_Virsorter2Db_RbsCategoryFormat(self):
        filepath = self.get_data_path("type/database/rbs/rbs-catetory.tsv")
        format = RbsCatetoryFormat(filepath, mode="r")
        format.validate()

    def test_Virsorter2Db_HallmarkGeneListFormat(self):
        filepath = self.get_data_path(
            "type/database/group/dsDNAphage/hallmark-gene.list"
        )
        format = HallmarkGeneListFormat(filepath, mode="r")
        format.validate()

    def test_GeneralFileFormat(self):
        filepath = self.get_data_path("type/database/group/dsDNAphage/model")
        format = GeneralFileFormat(filepath, mode="r")
        format.validate()

    def test_Virsorter2DbDirFmt(self):
        filepath = self.get_data_path("type/database/")
        format = Virsorter2DbDirFmt(filepath, mode="r")
        format.validate()

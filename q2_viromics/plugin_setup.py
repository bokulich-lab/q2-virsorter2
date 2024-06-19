# ----------------------------------------------------------------------------
# Copyright (c) 2024, Christos Matzoros.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Citations, Plugin
from q2_types.feature_data import FeatureData, Sequence
from q2_viromics import __version__
# from q2_viromics._virsorter2 import virsorter2_fetch_db

from q2_viromics.types._format import (
    Virsorter2DbDirFmt,
)
from q2_viromics.types._type import Virsorter2Db

citations = Citations.load("citations.bib", package="q2_viromics")

plugin = Plugin(
    name="viromics",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-viromics",
    package="q2_viromics",
    description="A QIIME 2 plugin for viromics analysis.",
    short_description="A QIIME 2 plugin for viromics analysis.",
    citations=[citations['Caporaso-Bolyen-2024']]
)

plugin.register_formats(
    Virsorter2DbDirFmt,
)
plugin.register_semantic_types(Virsorter2Db)

plugin.register_artifact_class(
    Virsorter2Db,
    directory_format=Virsorter2DbDirFmt,
    description=(
        "Represents a group Virsorter2 database."
    ),
)

"""
plugin.methods.register_function(
    function=virsorter2_fetch_db,
    inputs={},
    parameters={},
    outputs=[('virsorter2_database', FeatureData[Sequence])],
    parameter_descriptions={},
    output_descriptions={'virsorter2_database': 'The duplicated feature table.'},
    name='Virsorter2 database',
    description=("Fetch a Virsorter2 database that includes a collection of known "
                "viral genomes and key genes that are typically found in viral genomes."),
    citations=[]
)
"""
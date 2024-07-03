# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import importlib

from q2_types.feature_data import FeatureData, Sequence
from qiime2.plugin import Citations, Int, Plugin, Range

from q2_viromics import __version__
from q2_viromics.types._format import (
    ViralBoundaryDirFmt,
    ViralBoundaryFmt,
    ViralScoreDirFmt,
    ViralScoreFmt,
    Virsorter2DbDirFmt,
)
from q2_viromics.types._type import ViralBoundary, ViralScore, Virsorter2Db
from q2_viromics.virsorter2_fetch_db import virsorter2_fetch_db
from q2_viromics.virsorter2_run import _virsorter2_analysis, virsorter2_run

citations = Citations.load("citations.bib", package="q2_viromics")

plugin = Plugin(
    name="viromics",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-viromics",
    package="q2_viromics",
    description="A QIIME 2 plugin for viromics analysis.",
    short_description="A QIIME 2 plugin for viromics analysis.",
    citations=[citations["Caporaso-Bolyen-2024"]],
)

plugin.register_formats(
    Virsorter2DbDirFmt,
    ViralScoreFmt,
    ViralScoreDirFmt,
    ViralBoundaryFmt,
    ViralBoundaryDirFmt,
)

plugin.register_semantic_types(Virsorter2Db, ViralScore)

plugin.register_artifact_class(
    Virsorter2Db,
    directory_format=Virsorter2DbDirFmt,
    description=("Represents a VirSorter2 database."),
)

plugin.register_artifact_class(
    FeatureData[ViralScore],
    directory_format=ViralScoreDirFmt,
    description=("Represents viral score table from VirSorter2."),
)

plugin.register_artifact_class(
    FeatureData[ViralBoundary],
    directory_format=ViralBoundaryDirFmt,
    description=("Represents viral boundary table from VirSorter2."),
)


plugin.methods.register_function(
    function=virsorter2_fetch_db,
    inputs={},
    parameters={
        "n_jobs": Int % Range(1, None),
    },
    outputs=[("database", Virsorter2Db)],
    parameter_descriptions={
        "n_jobs": "Number of simultaneous downloads.",
    },
    output_descriptions={"database": "Virsorter2 database."},
    name="Fetch virsorter2 database.",
    description=(
        "Fetch a Virsorter2 database that includes a collection "
        "of known viral genomes and key genes that are typically "
        "found in viral genomes."
    ),
    citations=[],
)


plugin.pipelines.register_function(
    function=virsorter2_run,
    inputs={
        "sequences": FeatureData[Sequence],
        "database": Virsorter2Db,
    },
    parameters={"n_jobs": Int % Range(1, None)},
    input_descriptions={
        "sequences": "Input sequences from an assembly or genome "
        "data for virus detection.",
        "database": "VirSorter2 database.",
    },
    parameter_descriptions={
        "n_jobs": "Max number of jobs allowed in parallel.",
    },
    outputs=[
        ("viral_sequences", FeatureData[Sequence]),
        ("viral_score", FeatureData[ViralScore]),
        ("viral_boundary", FeatureData[ViralBoundary]),
    ],
    output_descriptions={
        "viral_sequences": "Identified viral sequences.",
        "viral_score": "Viral score table.",
        "viral_boundary": "Viral boundary table.",
    },
    name="Identifying and vizualize statistics for viral sequences.",
    description="Performs analysis for identifying and categorizing viral "
    "sequences from metagenomic data using VirSorter2 and provides "
    "useful visualizations.",
    citations=[],
)

plugin.methods.register_function(
    function=_virsorter2_analysis,
    inputs={
        "sequences": FeatureData[Sequence],
        "database": Virsorter2Db,
    },
    parameters={"n_jobs": Int % Range(1, None)},
    input_descriptions={
        "sequences": "Input sequences from an assembly or genome "
        "data for virus detection.",
        "database": "VirSorter2 database.",
    },
    parameter_descriptions={"n_jobs": "Max number of jobs allowed in parallel."},
    outputs=[
        ("viral_sequences", FeatureData[Sequence]),
        ("viral_score", FeatureData[ViralScore]),
        ("viral_boundary", FeatureData[ViralBoundary]),
    ],
    output_descriptions={
        "viral_sequences": "Identified viral sequences.",
        "viral_score": "Viral score table.",
        "viral_boundary": "Viral boundary table.",
    },
    name="Identifying and vizualize statistics for viral sequences.",
    description="Performs analysis for identifying and categorizing viral "
    "sequences from metagenomic data using VirSorter2 and provides "
    "useful visualizations.",
    citations=[],
)

importlib.import_module("q2_viromics.types._transformer")

# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from q2_types.feature_data import FeatureData, Sequence
from q2_types.metadata import ImmutableMetadata
from qiime2.plugin import Citations, Float, Int, Plugin, Range

from q2_virsorter2 import __version__
from q2_virsorter2.types._format import Virsorter2DbDirFmt
from q2_virsorter2.types._type import Virsorter2Db
from q2_virsorter2.virsorter2_fetch_db import fetch_db
from q2_virsorter2.virsorter2_run import run

citations = Citations.load("citations.bib", package="q2_virsorter2")

plugin = Plugin(
    name="virsorter2",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-virsorter2",
    package="q2_virsorter2",
    description="A QIIME 2 plugin for virsorter2 analysis.",
    short_description="A QIIME 2 plugin for virsorter2 analysis.",
    citations=[citations["Caporaso-Bolyen-2024"]],
)

plugin.register_formats(
    Virsorter2DbDirFmt,
)

plugin.register_semantic_types(Virsorter2Db)

plugin.register_artifact_class(
    Virsorter2Db,
    directory_format=Virsorter2DbDirFmt,
    description=("VirSorter2 database."),
)

plugin.methods.register_function(
    function=fetch_db,
    inputs={},
    parameters={
        "n_jobs": Int % Range(1, None),
    },
    outputs=[("database", Virsorter2Db)],
    parameter_descriptions={
        "n_jobs": "Number of simultaneous downloads.",
    },
    output_descriptions={"database": "Virsorter2 database."},
    name="Fetch virsorter2 database",
    description=(
        "Fetch a Virsorter2 database that includes a collection "
        "of known viral genomes and key genes that are typically "
        "found in viral genomes."
    ),
    citations=[citations["VirSorter2"]],
)

plugin.methods.register_function(
    function=run,
    inputs={
        "sequences": FeatureData[Sequence],
        "database": Virsorter2Db,
    },
    parameters={
        "n_jobs": Int % Range(1, None),
        "min_score": Float % Range(0, 1),
        "min_length": Int % Range(0, None),
    },
    input_descriptions={
        "sequences": "Input sequences from an assembly or genome "
        "data for virus detection.",
        "database": "VirSorter2 database.",
    },
    parameter_descriptions={
        "n_jobs": "Max number of jobs allowed in parallel.",
        "min_score": "Minimal score to be identified as viral.",
        "min_length": "Minimal sequence length required. All sequences "
        "shorter than this will "
        "be removed.",
    },
    outputs=[
        ("viral_sequences", FeatureData[Sequence]),
        ("viral_score", ImmutableMetadata),
        ("viral_boundary", ImmutableMetadata),
    ],
    output_descriptions={
        "viral_sequences": "Identified viral sequences.",
        "viral_score": "Viral score table.",
        "viral_boundary": "Viral boundary table.",
    },
    name="Identify viral sequences and produce corresponding metadata",
    description="Performs analysis for identifying and categorizing viral "
    "sequences from metagenomic data using VirSorter2 and provides "
    "corresponding metadata data.",
    citations=[citations["VirSorter2"]],
)

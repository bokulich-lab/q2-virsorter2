# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Citations, Int, Plugin, Range

from q2_viromics import __version__
from q2_viromics.types._format import Virsorter2DbDirFmt
from q2_viromics.types._type import Virsorter2Db
from q2_viromics.virsorter2_fetch_db import virsorter2_fetch_db

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
)
plugin.register_semantic_types(Virsorter2Db)

plugin.register_artifact_class(
    Virsorter2Db,
    directory_format=Virsorter2DbDirFmt,
    description=("Represents a group Virsorter2 database."),
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

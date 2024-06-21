# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import shutil
import subprocess

from q2_viromics._utils import run_command
from q2_viromics.types._format import Virsorter2DbDirFmt


# Create the command to fetch the Virsorter2 database
def create_fetch_db_cmd(database, n_jobs):
    build_cmd = [
        "virsorter",
        "setup",
        "-d",
        str(database.path),
        "-s",
        "-j",
        str(n_jobs),
    ]

    return build_cmd


# Delete a directory and its contents if it exists.
def delete_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)


# Fetch the Virsorter2 database
def virsorter2_fetch_db(n_jobs: int = 10) -> Virsorter2DbDirFmt:
    # Initialize a directory format object to store the Minimap2 index
    database = Virsorter2DbDirFmt()

    # Construct the command to build the Minimap2 index file
    fetch_db_cmd = create_fetch_db_cmd(database, n_jobs)

    try:
        # Execute the command to create the Minimap2 index database
        run_command(fetch_db_cmd)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running virsorter2 setup, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )

    # Clean up the unnecessary directories
    for dir_name in [".snakemake", "conda_envs"]:
        delete_directory(os.path.join(str(database.path), dir_name))

    return database

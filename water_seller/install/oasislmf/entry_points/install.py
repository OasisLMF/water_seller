"""
This file defines the entry point for building ktools locally and installing OasisLMF.
"""
import os
import shutil
import argparse

from water_seller.install.oasislmf.steps.clone_repos import CloneRepos
from water_seller.install.oasislmf.steps.compile_ktools import CompileKtools
from water_seller.install.oasislmf.steps.install_oasislmf import InstallOasisLmf
from water_seller.install.oasislmf.steps.package_ktools import PackageKtools


def main() -> None:
    """
    The main function for building ktools and installing oasislmf.
    """
    parser = argparse.ArgumentParser(description="Example script using argparse")

    # Add the extra flag, store_true sets the value to True if the flag is present, otherwise False
    parser.add_argument(
        "--extra",
        dest="extra",
        action="store_true",
        help="If extra OasisLMF requirements are installed Use this flag to set the value to True"
    )

    args = parser.parse_args()

    root_path: str = str(os.getcwd())
    stash_path: str = str(os.path.join(root_path, "stash"))

    if os.path.exists(stash_path):
        shutil.rmtree(stash_path)
    os.mkdir(stash_path)

    clone_ktools: CloneRepos = CloneRepos(
        root_path=root_path,
        git_url="https://github.com/OasisLMF/ktools.git",
        package_name="ktools"
    )
    clone_ktools.clone_repo()

    compile_ktools: CompileKtools = CompileKtools(ktools_path=clone_ktools.package_path)
    compile_ktools.compile()

    package_ktools: PackageKtools = PackageKtools(ktools_path=clone_ktools.package_path)
    package_ktools.package()

    clone_oasislmf: CloneRepos = CloneRepos(
        root_path=root_path,
        git_url="https://github.com/OasisLMF/OasisLMF.git",
        package_name="oasislmf"
    )
    clone_oasislmf.clone_repo()

    install_oasislmf: InstallOasisLmf = InstallOasisLmf(root_path=clone_oasislmf.package_path,
                                                        ktools_path=clone_ktools.package_path,
                                                        extra=args.extra)
    install_oasislmf.install()
    shutil.rmtree(stash_path)

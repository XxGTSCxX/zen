import os
import argparse
import helpers


# Configuring Argument Parser --------------------------------------------------
parser: argparse.ArgumentParser = argparse.ArgumentParser(
    prog="project_builder",
    description="Runs the build commands to compile the project.",
)
parser.add_argument(
    "--project-name",
    help="The name of this project.",
    dest="project_name",
    required=True,
)
parser.add_argument(
    "--build-type",
    help="Build and packaging settings.",
    dest="build_type",
    choices=["Release", "RelWithDebInfo", "Debug"],
    required=True,
)
parser.add_argument(
    "--build-folder",
    "-bf",
    dest="build_dir",
    help="Target directory for build config files to be put in.",
    required=True,
)
parser.add_argument(
    "--output-folder",
    "-of",
    dest="output_dir",
    help="Target directory for build outputs to be put in.",
    required=True,
)
parser.add_argument(
    "--project-folder",
    "-pf",
    dest="project_dir",
    help="Project directory with all of the source files.",
    required=True,
)
parser.add_argument(
    "--options",
    "-o",
    dest="options",
    help="Options to be forwarded to the conan recipe.",
    action="append",
)
args: argparse.Namespace = parser.parse_args()


# Validate Arguments -----------------------------------------------------------
if not os.path.exists(args.project_dir):
    raise AssertionError(f"Invalid project directory: {args.project_dir}")
os.makedirs(f"{args.output_dir}/{args.build_type.lower()}", exist_ok=True)
os.makedirs(f"{args.build_dir}/{args.build_type.lower()}", exist_ok=True)


# Execute Conan Commands -------------------------------------------------------
profile_prefix: str = f"{args.project_dir}/build_profiles/{args.project_name.lower()}"
curr_profile: str = f"{profile_prefix}_current"
used_profile: str = f"{profile_prefix}_{args.build_type.lower()}"
if not os.path.isfile(curr_profile):
    os.system(f"conan profile new {curr_profile} --detect")
os.system(
    f"conan install {args.project_dir} "
    f"--build=outdated "
    f"-if {args.build_dir}/{args.build_type.lower()} "
    f"-of {args.build_dir}/{args.build_type.lower()} "
    f"-pr:b {used_profile} "
    f"-pr:h {used_profile} "
    f"{helpers.parse_options(args)}"
)
os.system(
    f"conan build {args.project_dir} "
    f"-if {args.build_dir}/{args.build_type.lower()} "
    f"-bf {args.output_dir}/{args.build_type.lower()}"
)

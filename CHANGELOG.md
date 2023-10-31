# Change Log
CHANGELOG.md format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Given a version number `MAJOR.MINOR.PATCH`, increment the:
> * `MAJOR` version when you make incompatible API changes (e.g. removing APIs).
> * `MINOR` version when you add functionality in a backwards compatible manner.
> * `PATCH` version when you make backwards compatible bug fixes.

**Dev Notes:** Using the `[[deprecated]]` attribute is still considered a minor change as long as you don't remove the interface.

| Tag | Description |
|-|-|
| VS Code | Any changes related to the Visual Studio Code experience, from VS Code extensions to project settings. |
| CMake | Any changes to the CMake files like CMakeLists.txt or config.hpp.in. |
| Conan | Any changes related to the Conan configurations. |
| Docs | Any changes to documentation files (.md). |

---
## [Unreleased]

### Added
* **[VS Code]** Project configuration.
  * Added `c_cpp_properties.json` for C/C++ extention configurations. Helps with locating include headers, predictive search, and intellisense.
  * Added `launch.json` for launch tasks. Currently only has launch tasks for test build since `zen_core` is meant to be a library.
  * Added `settings.json` for project-based settings so that project formatting can be as consistent as possible.
  * Added `tasks.json` for any project tasks. Currently has project setup task, and build tasks for library and test build.
  * Added `.clang-format` for C/C++ file formatting.
  * Added `.gitignore` for ignore directories and files.
  * Added `requirements.txt` for `"Install Zen Development Requirements"` setup task.
  * Added `build_scripts/build.py` to help with building the project for local testing - uses conan internally.
  * Added `build_scripts/helpers.py` for `build.py` helpers.
* **[CMake]** CMakeLists.txt setup.
  * Setup project file directories for CMake to build and link the project.
  * Created CMake macro `add_test_sources` for adding sources to test executable in any subdirectories so that test sources can be added only if the subdirectory is included. This is useful for only testing included features (that are included as subdirectories) when toggleable features are enabled.
  * Set `include` directory to be `PUBLIC` include, while `src` directory is `PRIVATE` include to make things cleaner for users to include.
* **[Conan]** Added conan configuration files.
  * Added `conanfile.py` for project recipe.
  * Added `build_profiles/*` for conan profiles that can be used for local builds.
* **[Docs]** Added documentations for the project.
  * `README.md` to help with understanding the project's purpose and development setup.
  * `CHANGELOG.md` to log the changes.
  * `LICENSE` for the project.

# Zen
A project for learning how to setup:
* [x] [Semantic Versioning](https://semver.org/)
* [x] Cross-platform compatiblity
  * [x] Conan - using this to create the package recipe and what are its required packages.
  * [x] CMake - using this to setup the project settings.
  * [x] clang - using this to build the project.
* [ ] CI/CD pipeline
  * [ ] Travis CI - using this to process the automated testings.
* [ ] ECS design
* [ ] Differred shading

## Versioning
For this project, [Semantic Versioning](https://semver.org/) is used.

> Given a version number `MAJOR.MINOR.PATCH`, increment the:
> * `MAJOR` version when you make incompatible API changes (e.g. removing APIs).
> * `MINOR` version when you add functionality in a backwards compatible manner.
> * `PATCH` version when you make backwards compatible bug fixes.

**Dev Notes:** Using the `[[deprecated]]` attribute is still considered a minor change as long as you don't remove the interface.

## Developer Setup
### 1. Install Required Packages
* [clang](https://github.com/llvm/llvm-project/releases) (use version 12 onwards)
  * Feel free to use any package manager (homebrew/chocolatey/apt-get) as long as you export you export the environment variables `CC` with your path to the `clang` executable and `CXX` with your path to the `clang++` executable so that CMake can locate the executables.
* [CMake](https://cmake.org/install/) (use version 3.2 onwards)
* [Ninja](https://github.com/ninja-build/ninja/releases) (use version 1.10.2 onwards)
* [Python](https://www.python.org/downloads/) (use version 3.2 onwards)
* (optional) [Visual Studio Code](https://code.visualstudio.com/download)
  * Cross-platform text editor that this project is configured for development on.
  * **NOTE:** DO NOT commit changes related to personal user configurations.
* (optional) [Visual Studio](https://visualstudio.microsoft.com/vs/older-downloads/) (currently only tested on version 16 (2019))
  * Only required for Windows build because direct lldb debugging is currently not supported on Visual Studio Code ([issue](https://github.com/microsoft/vscode-cpptools/issues/6617)).

### 2. Run Build Command "Install Requirements"
Run the build command "Install Requirements" to install the list of packages that can be installed with Python, and the Python modules that the Python scripts in this project will use. Naturally, this will require you to have installed Python.

from conans import ConanFile, CMake
import os


# List of optional features ----------------------------------------------------
optional_features = ["testing"]
macro_definitions = {"NOMINMAX": True}


# Helpers ----------------------------------------------------------------------
def generate_config_file(config_file_dir: str):
    config_file_path: str = os.path.join(config_file_dir, "src/config.hpp.in")
    macro_defines: str = ""
    feature_defines: str = ""
    open_permission: str = "x"
    for macro_name in macro_definitions.keys():
        macro_defines = f"{macro_defines}#cmakedefine {macro_name}\n"
    for feature_name in optional_features:
        macro_name = f"ZEN_WITH_{feature_name.upper()}"
        feature_defines = f"{feature_defines}#cmakedefine {macro_name}\n"
    if os.path.isfile(config_file_path):
        open_permission = "w"
    with open(config_file_path, open_permission) as config_file:
        config_file.write(
            "#ifndef ZEN_CONFIG_HPP\n"
            "#define ZEN_CONFIG_HPP\n"
            "\n"
            "#define ZEN_VERSION_MAJOR @zen_VERSION_MAJOR@\n"
            "#define ZEN_VERSION_MINOR @zen_VERSION_MINOR@\n"
            "#define ZEN_VERSION_PATCH @zen_VERSION_PATCH@\n"
            "\n"
            f"{macro_defines}"
            f"{feature_defines}"
            "\n"
            "#endif  // #ifndef ZEN_CONFIG_HPP\n"
        )


class ZenConan(ConanFile):
    # ConanFile Members --------------------------------------------------------
    name = "zen"
    version = "0.0.0"
    description = "A project for learning."
    url = "https://github.com/XxGTSCxX/zen.git"
    license = "MIT"
    author = "Gabrielle Tan (gabrielle@gtsc.dev)"
    settings = "os", "compiler", "build_type", "arch"
    generators = ["cmake"]
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "is_contributor_build": [True, False],
    }
    options.update(
        {f"with_{feature_name}": [True, False] for feature_name in optional_features}
    )
    default_options = {
        "shared": False,
        "fPIC": True,
        "is_contributor_build": False,
    }
    default_options.update(
        {f"with_{feature_name}": False for feature_name in optional_features}
    )
    exports_sources = (
        "include/*",
        "src/*",
        "CMakeLists.txt",
        "!src/config.hpp",
        "!src/config.hpp.in",
    )

    # Private Custom Members ---------------------------------------------------
    _generate_config: bool = False
    _config_file_path: str = None
    _cmake: CMake = None

    # ConanFile Methods In Invocation Order ------------------------------------
    def configure(self):
        if self.options.is_contributor_build:
            self._generate_config = True
            self._config_file_path = os.path.abspath(os.path.curdir)

    def requirements(self):
        if self.options.with_testing:
            self.requires("catch2/3.3.2")

    def build_requirements(self):
        pass

    def source(self):
        self._generate_config = True

    def build(self):
        if self._generate_config and self._config_file_path == None:
            self._config_file_path = os.path.abspath(os.path.curdir)
        generate_config_file(self._config_file_path)
        if self._cmake == None:
            self._cmake = CMake(self, generator="Ninja")
        if self.should_configure:
            self._cmake.definitions["CONAN_INSTALL_DIR"] = self.install_folder
            for macro_name, is_defined in macro_definitions.items():
                self._cmake.definitions[macro_name] = is_defined
            for feature_name in optional_features:
                macro_name: str = f"ZEN_WITH_{feature_name.upper()}"
                option_name: str = f"with_{feature_name}"
                feature_enabled: bool = getattr(self.options, option_name, False)
                self._cmake.definitions[macro_name] = feature_enabled
            self._cmake.configure()
        if self.should_build:
            self._cmake.build()

    def package(self):
        if self._cmake == None:
            self._cmake = CMake(self, generator="Ninja")
        self._cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libs = ["zen_core"]
        for feature_name in optional_features:
            option_name: str = f"with_{feature_name}"
            if getattr(self.options, option_name, False):
                self.cpp_info.libs.append(f"zen_{feature_name}")

from conans import ConanFile, CMake
from shutil import rmtree

class Exiv2Conan(ConanFile):
    name = "Exiv2"
    version = "0.26"
    description = "A C++ library and a command line utility to read and write Exif, IPTC and XMP image metadata"
    license = "GNU GPL2"
    url = "https://github.com/Exiv2/exiv2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = ["FindExiv2.cmake"]

    def source(self):
        self.run("git clone --depth 1 --branch v%s https://github.com/Exiv2/exiv2.git" % self.version)

    def build(self):
        cmake = CMake(self, parallel=True)

        cmake_args = {"EXIV2_ENABLE_NLS" : "OFF",
                      "EXIV2_ENABLE_LENSDATA" : "OFF",
                      "EXIV2_ENABLE_COMMERCIAL" : "OFF",
                      "EXIV2_ENABLE_VIDEO" : "OFF",
                      "EXIV2_ENABLE_WEBREADY" : "OFF",
                      "EXIV2_ENABLE_CURL" : "OFF",
                      "EXIV2_ENABLE_SSH" : "OFF",
                      "EXIV2_ENABLE_BUILD_SAMPLES" : "OFF",
                      "EXIV2_ENABLE_BUILD_PO" : "OFF",
                      "EXIV2_ENABLE_SHARED" : "ON",
                      "EXIV2_ENABLE_XMP" : "ON",
                      "EXIV2_ENABLE_PNG" : "ON",
                      "CMAKE_INSTALL_PREFIX" : self.package_folder
                     }

        cmake.configure(source_dir="../exiv2", build_dir="build", defs=cmake_args)
        cmake.build(target="install")

    def package(self):
        self.copy("FindExiv2.cmake", ".", ".")
        #if self.settings.os != "Windows":
        #    rmtree(self.package_folder + '/bin')
        #rmtree(self.package_folder + '/man')

    def package_info(self):
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libs = ['exiv2']  # The libs to link against
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found

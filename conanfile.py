from conans import ConanFile, tools, CMake


class Exiv2Conan(ConanFile):
    name = "Exiv2"
    version = "0.26"
    description = "A C++ library and a command line utility to read and write Exif, IPTC and XMP image metadata"
    license = "GNU GPL2"
    url = "https://github.com/Exiv2/exiv2"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "commercial": [True, False],
        "xmp": [True, False],
        "png": [True, False],
        "ssh": [True, False],
        "curl": [True, False],
        "webready": [True, False],
        "video": [True, False],
        "lensdata": [True, False],
        "nls": [True, False],
        "unicode": [True, False]
    }

    default_options = "commercial=False", \
        "xmp=True", \
        "png=True", \
        "ssh=False", \
        "curl=False", \
        "webready=False", \
        "video=False", \
        "lensdata=False", \
        "unicode=True", \
        "shared=True", \
        "nls=False"

    generators = "cmake"
    exports = ["FindExiv2.cmake"]

    def requirements(self):
        self.requires("zlib/1.2.11@conan/stable")
        self.requires("Expat/2.2.1@piponazo/testing")

    def configure(self):
        self.options["zlib"].shared = self.options.shared
        self.options["Expat"].shared = self.options.shared

    def source(self):
        self.run("git clone --depth 1 --branch v%s https://github.com/Exiv2/exiv2.git" % self.version)
        tools.replace_in_file("exiv2/CMakeLists.txt", "PROJECT( exiv2 )", '''PROJECT( exiv2 )
            include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
            conan_basic_setup()''')

    def build(self):
        cmake = CMake(self, parallel=True)

        cmake_args = {"EXIV2_ENABLE_NLS" : self.options.nls,
                      "EXIV2_ENABLE_LENSDATA" : self.options.lensdata,
                      "EXIV2_ENABLE_COMMERCIAL" : self.options.commercial,
                      "EXIV2_ENABLE_VIDEO" : self.options.video,
                      "EXIV2_ENABLE_WEBREADY" : self.options.webready,
                      "EXIV2_ENABLE_CURL" : self.options.curl,
                      "EXIV2_ENABLE_SSH" : self.options.ssh,
                      "EXIV2_ENABLE_BUILD_SAMPLES" : "OFF",
                      "EXIV2_ENABLE_BUILD_PO" : "OFF",
                      "EXIV2_ENABLE_SHARED" : self.options.shared,
                      "EXIV2_ENABLE_XMP" : self.options.xmp,
                      "EXIV2_ENABLE_PNG" : self.options.png,

                      # It cannot be disabled in the version 0.26. The compilation will fail.
                      # The problem has been fixed on master.
                      "EXIV2_ENABLE_LIBXMP" : "ON",

                      "CMAKE_INSTALL_PREFIX" : self.package_folder
                     }

        if tools.os_info.is_windows:
            cmake_args['EXIV2_ENABLE_WIN_UNICODE'] = self.options.unicode

        cmake.configure(source_dir="../exiv2", build_dir="build", defs=cmake_args)
        cmake.build(target="install")

    def package(self):
        self.copy("FindExiv2.cmake", ".", ".")

    def package_info(self):
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.debug.libs = ["exiv2d"]
        self.cpp_info.release.libs = ["exiv2"]
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found

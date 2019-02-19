from conans import ConanFile, tools, CMake


class Exiv2Conan(ConanFile):
    name = "Exiv2"
    version = "0.27"
    description = "A C++ library and a command line utility to read and write Exif, IPTC and XMP image metadata"
    license = "GNU GPL2"
    url = "https://github.com/Exiv2/exiv2"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "xmp": [True, False],
        "png": [True, False],
        "ssh": [True, False],
        "curl": [True, False],
        "webready": [True, False],
        "video": [True, False],
        "lensdata": [True, False],
        "nls": [True, False],
        "buildTool": [True, False],
        "unicode": [True, False]
    }

    default_options = {"xmp": True,
                       "png": True,
                       "ssh": False,
                       "curl": False,
                       "webready": False,
                       "video": False,
                       "lensdata": False,
                       "unicode": True,
                       "shared": True,
                       "buildTool": True,
                       "nls": False,
    }

    generators = "cmake"

    def requirements(self):
        self.requires("zlib/1.2.11@conan/stable")
        self.requires("Expat/2.2.6@pix4d/testing")

    def source(self):
        self.run("git clone --depth 1 --branch 0.27 https://github.com/Exiv2/exiv2.git")

    def build(self):
        tools.replace_in_file("exiv2/cmake/findDependencies.cmake", "conanbuildinfo.cmake)", "../conanbuildinfo.cmake)")

        cmake = CMake(self)

        cmake_args = {"EXIV2_ENABLE_NLS" : self.options.nls,
                      "EXIV2_ENABLE_LENSDATA" : self.options.lensdata,
                      "EXIV2_ENABLE_VIDEO" : self.options.video,
                      "EXIV2_ENABLE_WEBREADY" : self.options.webready,
                      "EXIV2_ENABLE_CURL" : self.options.curl,
                      "EXIV2_ENABLE_SSH" : self.options.ssh,
                      "EXIV2_BUILD_SAMPLES" : "OFF",
                      "EXIV2_BUILD_EXIV2_COMMAND": self.options.buildTool,
                      "EXIV2_BUILD_PO" : "OFF",
                      "EXIV2_ENABLE_XMP" : self.options.xmp,
                      "EXIV2_ENABLE_PNG" : self.options.png,
                      "CMAKE_INSTALL_PREFIX" : self.package_folder
                     }

        if tools.os_info.is_windows:
            cmake_args['EXIV2_ENABLE_WIN_UNICODE'] = self.options.unicode

        cmake.configure(source_dir="../exiv2", build_dir="build", defs=cmake_args)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.debug.libs = ["exiv2d"]
        self.cpp_info.release.libs = ["exiv2"]
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found

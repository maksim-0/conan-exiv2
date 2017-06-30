from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "piponazo")

class Exiv2TestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "Exiv2/0.26@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.definitions.pop("CONAN_C_FLAGS")
        cmake.definitions.pop("CONAN_CXX_FLAGS")

        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        data_file = os.path.join(self.conanfile_directory, "dji_inspire_xmp_fake.jpg")
        if self.settings.os == "Windows":
            self.run("cd bin/%s && .%stestApp %s" % (self.settings.build_type, os.sep, data_file))
        else:
            self.run(".%s/bin/testApp %s" % (os.sep, data_file))

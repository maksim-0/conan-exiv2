from conans import ConanFile, CMake
import os

class Exiv2TestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="lib", src="lib")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        data_file = os.path.join(self.source_folder, "dji_inspire_xmp_fake.jpg")
        self.run("%s %s" % (os.sep.join(['bin', 'testApp']), data_file))

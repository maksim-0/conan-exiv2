from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="piponazo", channel="testing")
    builder.add_common_builds()
    #builder.add_common_builds(shared_option_name="Exiv2:shared")
    builder.run()

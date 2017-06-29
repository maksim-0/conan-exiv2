# - Try to find the Exiv2 library

find_path(EXIV2_INCLUDE_DIRS NAMES exiv2/exiv2.hpp PATHS ${CONAN_INCLUDE_DIRS_EXIV2})
find_library(EXIV2_LIBRARIES NAMES ${CONAN_LIBS_EXIV2} PATHS ${CONAN_LIB_DIRS_EXIV2})

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Exiv2 DEFAULT_MSG EXIV2_INCLUDE_DIRS EXIV2_LIBRARIES)

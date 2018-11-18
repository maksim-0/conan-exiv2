cmake_minimum_required(VERSION 3.8)
project(Exiv2Test CXX)

set(CMAKE_CXX_STANDARD 11)
set(CXX_STANDARD_REQUIRED ON)

if (UNIX) # Assuming the usage of gcc or clang compilers
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
endif()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()
conan_basic_setup(NO_OUTPUT_DIRS KEEP_RPATHS TARGETS)


find_package(exiv2 REQUIRED CONFIG)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(testApp main.cpp)
target_link_libraries(testApp exiv2lib)

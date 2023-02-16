#cmake_minimum_required(VERSION 3.20)
#project(selection_tools)
#
#set(CMAKE_CXX_STANDARD 14)
#
##list(APPEND CMAKE_PREFIX_PATH $ENV{ROOTSYS})
#
#find_package(ROOT REQUIRED COMPONENTS RIO Net)
#include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
#
#find_package(ROOT)
#include(${ROOT_USE_FILE})
#
##SET(CMAKE_SKIP_BUILD_RPATH FALSE)
##SET(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
##SET(CMAKE_INSTALL_RPATH "/cvmfs/sft.cern.ch/lcg/releases/vdt/0.4.3-992df/x86_64-centos7-gcc8-opt/lib:/cvmfs/sft.cern.ch/lcg/releases/tbb/2019_U7-ba3eb/x86_64-centos7-gcc8-opt/lib:/cvmfs/sft.cern.ch/lcg/releases/Davix/0.7.3-d94fa/x86_64-centos7-gcc8-opt/lib64/:/cvmfs/sft.cern.ch/lcg/releases/png/1.6.37-9c2fe/x86_64-centos7-gcc8-opt/lib/:/cvmfs/sft.cern.ch/lcg/releases/GSL/2.5-32fc5/x86_64-centos7-gcc8-opt/lib/")
##SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
#
#add_library(Analysis SHARED src/Particle.cpp)
#target_link_libraries(Analysis PUBLIC ${ROOT_LIBRARIES})
#
#
#add_executable(apply_selections apply_selections.C)
#set_property(TARGET apply_selections PROPERTY CXX_STANDARD 14)
#target_link_libraries(apply_selections Analysis)
#
#include_directories("${PROJECT_SOURCE_DIR}/include")



cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(apply_selections)

# Locate the ROOT package and define a number of useful targets and variables.
find_package(ROOT REQUIRED COMPONENTS RIO Net)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Create a shared library.
# Passing cmake targets such as `ROOT::RIO` as dependencies (rather than plain
# library names for example via ${ROOT_LIBRARIES}) ensures that properties such as required
# include directories and C++ standard are propagated to our libraries or executables.
# Note: To ensure compatibility with Cling, targets *must* be compiled using the
# same C++ standard as ROOT was compiled with.
add_library(Analysis SHARED src/Particle.cpp)
target_link_libraries(Analysis PUBLIC ROOT::RIO ROOT::Net)

# Create the main program using the library.
add_executable(apply_selections apply_selections.C)
target_link_libraries(apply_selections Analysis)

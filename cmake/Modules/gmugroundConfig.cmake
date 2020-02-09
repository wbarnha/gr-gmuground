INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_GMUGROUND gmuground)

FIND_PATH(
    GMUGROUND_INCLUDE_DIRS
    NAMES gmuground/api.h
    HINTS $ENV{GMUGROUND_DIR}/include
        ${PC_GMUGROUND_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GMUGROUND_LIBRARIES
    NAMES gnuradio-gmuground
    HINTS $ENV{GMUGROUND_DIR}/lib
        ${PC_GMUGROUND_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gmugroundTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GMUGROUND DEFAULT_MSG GMUGROUND_LIBRARIES GMUGROUND_INCLUDE_DIRS)
MARK_AS_ADVANCED(GMUGROUND_LIBRARIES GMUGROUND_INCLUDE_DIRS)

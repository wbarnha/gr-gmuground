# Install script for directory: /home/wbarnhart/gr-gmuground/python

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/gmuground" TYPE FILE FILES
    "/home/wbarnhart/gr-gmuground/python/__init__.py"
    "/home/wbarnhart/gr-gmuground/python/sqrt.py"
    "/home/wbarnhart/gr-gmuground/python/snr_selector.py"
    "/home/wbarnhart/gr-gmuground/python/sample_count.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/gmuground" TYPE FILE FILES
    "/home/wbarnhart/gr-gmuground/build/python/__init__.pyc"
    "/home/wbarnhart/gr-gmuground/build/python/sqrt.pyc"
    "/home/wbarnhart/gr-gmuground/build/python/snr_selector.pyc"
    "/home/wbarnhart/gr-gmuground/build/python/sample_count.pyc"
    "/home/wbarnhart/gr-gmuground/build/python/__init__.pyo"
    "/home/wbarnhart/gr-gmuground/build/python/sqrt.pyo"
    "/home/wbarnhart/gr-gmuground/build/python/snr_selector.pyo"
    "/home/wbarnhart/gr-gmuground/build/python/sample_count.pyo"
    )
endif()


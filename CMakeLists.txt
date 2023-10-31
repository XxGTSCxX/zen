cmake_minimum_required(VERSION 3.2)

project(zen VERSION 0.0.0)

# Configuring Project ----------------------------------------------------------
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD_REQUIRED true)
set(CONFIG_FILE "config.hpp")

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/src/${CONFIG_FILE}.in ${CMAKE_CURRENT_SOURCE_DIR}/src/${CONFIG_FILE} @ONLY)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/${CONFIG_FILE} DESTINATION src/)

include(${CONAN_INSTALL_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

# Creating global read-only variables ------------------------------------------
set(ZEN_COMPILE_FLAGS -O2 -Wall -Wextra -Wpedantic -Werror)
set(ZEN_INCLUDE_DIR ${CMAKE_CURRENT_LIST_DIR}/include)
set(ZEN_SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/src)

# Creating global read-write variables -----------------------------------------
set_property(GLOBAL PROPERTY ZEN_REGISTERED_LIBS) # List of feature libraries to include for testing
set_property(GLOBAL PROPERTY ZEN_REGISTERED_TEST_SOURCES) # List of test sources to include for testing

# Define Helper Functions ------------------------------------------------------
function(AddZenLib FEATURE_NAME)
  set(LIB_NAME ${PROJECT_NAME}_${FEATURE_NAME})
  add_library(${LIB_NAME} ${ARGN})
  target_compile_options(${LIB_NAME} PRIVATE ${ZEN_COMPILE_FLAGS})
  target_include_directories(${LIB_NAME}
    INTERFACE ${ZEN_INCLUDE_DIR}
    PRIVATE ${ZEN_SOURCE_DIR}
  )
  install(TARGETS ${LIB_NAME}
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
  )
  install(DIRECTORY ${CMAKE_CURRENT_LIST_DIR} DESTINATION src/
    FILES_MATCHING
    PATTERN "*.hpp"
    PATTERN "*.inl"

    # Exclude test only headers.
    PATTERN "*.test.hpp" EXCLUDE
    PATTERN "*.test.inl" EXCLUDE

    # Exclude internal only headers.
    PATTERN "*.internal.hpp" EXCLUDE
    PATTERN "*.internal.inl" EXCLUDE

    # Exclude generated files.
    PATTERN "*.generated.hpp" EXCLUDE
    PATTERN "*.generated.inl" EXCLUDE
  )
  install(FILES
    ${ZEN_INCLUDE_DIR}/zen/${FEATURE_NAME}.hpp
    DESTINATION include/zen/
  )

  if(ZEN_WITH_TESTING)
    # Register library's name to link to test executable.
    get_property(REGISTERED_LIBS GLOBAL PROPERTY ZEN_REGISTERED_LIBS)
    list(APPEND REGISTERED_LIBS ${LIB_NAME})
    set_property(GLOBAL PROPERTY ZEN_REGISTERED_LIBS ${REGISTERED_LIBS})

    # Register library's source files to add to test executable.
    get_property(REGISTERED_TEST_SOURCES GLOBAL PROPERTY ZEN_REGISTERED_TEST_SOURCES)
    file(GLOB_RECURSE LIB_TEST_SOURCES "**.test.cpp")
    list(APPEND REGISTERED_TEST_SOURCES ${LIB_TEST_SOURCES})
    set_property(GLOBAL PROPERTY ZEN_REGISTERED_TEST_SOURCES ${REGISTERED_TEST_SOURCES})
  endif()
endfunction()

# March source directory for libs and test sources -----------------------------
add_subdirectory(src)

# Generate Test Executable -----------------------------------------------------
if(ZEN_WITH_TESTING)
  set(TEST_PROJECT_NAME ${PROJECT_NAME}_test)
  get_property(REGISTERED_LIBS GLOBAL PROPERTY ZEN_REGISTERED_LIBS)
  get_property(REGISTERED_TEST_SOURCES GLOBAL PROPERTY ZEN_REGISTERED_TEST_SOURCES)
  add_executable(${TEST_PROJECT_NAME} ${REGISTERED_TEST_SOURCES})
  target_compile_options(${TEST_PROJECT_NAME} PRIVATE ${ZEN_COMPILE_FLAGS})
  target_include_directories(${TEST_PROJECT_NAME} PRIVATE
    ${ZEN_INCLUDE_DIR}
    ${ZEN_SOURCE_DIR}
  )
  target_link_libraries(${TEST_PROJECT_NAME} PRIVATE
    CONAN_PKG::catch2
    ${REGISTERED_LIBS}
  )
endif()

// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

#ifndef TEST_UTILITY_HPP_
#define TEST_UTILITY_HPP_

#include <stdio.h>
#include <stdlib.h>

#include <fstream>

template <typename T>
void ReadBinaryFile(const char filename[], T* data) {
  std::ifstream fin(filename, std::ios::in | std::ios::binary | std::ios::ate);
  if (fin.fail()) {
    printf("Cannot open the file.");
    abort();
  }
  const auto file_size = static_cast<size_t>(fin.tellg());
  const auto type_size = sizeof(T);
  if (file_size % type_size != 0) {
    printf("Invalid file size.");
    abort();
  }
  fin.seekg(0, std::ios::beg);
  fin.read(static_cast<char*>(static_cast<void*>(data)),
           static_cast<std::streamsize>(file_size));
  fin.close();
}

#endif  // TEST_UTILITY_HPP_

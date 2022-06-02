// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

#include "ibex_super_system.h"

int main(int argc, char **argv) {
  SuperSystem super_system(
      "TOP.ibex_super_system.u_ram.u_ram.gen_generic.u_impl_generic",
      64 * 1024);

  return super_system.Main(argc, argv);
}

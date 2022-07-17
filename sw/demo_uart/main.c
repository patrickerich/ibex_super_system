#include <stdio.h>

#include "super_system.h"


int main(void) {

  // Initialization stuff
  int c = EOF;

  // Main loop
  while(1) {

    // Do other stuff


    if (is_char_waiting()) {
      c = getchar();
      putchar(c);
    }

    // Do other stuff

  }

}

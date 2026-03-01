#include "quiz3_solution.h"

#include <stdio.h>
#include <stdlib.h>

// tile_and_fused_blur(
//     W : size,
//     H : size,
//     blur_y : ui16[H, W] @DRAM,
//     inp : ui16[H + 2, W + 2] @DRAM
// )
void tile_and_fused_blur( void *ctxt, int_fast32_t W, int_fast32_t H, uint16_t* blur_y, const uint16_t* inp ) {
EXO_ASSUME(H % 32 == 0);
EXO_ASSUME(W % 256 == 0);
uint16_t *blur_x = (uint16_t*) malloc((2 + H) * W * sizeof(*blur_x));
for (int_fast32_t yo = 0; yo < ((H) / (32)); yo++) {
  for (int_fast32_t xo = 0; xo < ((W) / (256)); xo++) {
    for (int_fast32_t yi = 0; yi < 34; yi++) {
      for (int_fast32_t xi = 0; xi < 256; xi++) {
        blur_x[(yi + 32 * yo) * W + xi + 256 * xo] = (inp[(yi + 32 * yo) * (W + 2) + xi + 256 * xo] + inp[(yi + 32 * yo) * (W + 2) + 1 + xi + 256 * xo] + inp[(yi + 32 * yo) * (W + 2) + 2 + xi + 256 * xo]) / ((uint16_t) 3.0);
      }
    }
    for (int_fast32_t yi = 0; yi < 32; yi++) {
      for (int_fast32_t xi = 0; xi < 256; xi++) {
        blur_y[(yi + 32 * yo) * W + xi + 256 * xo] = (blur_x[(yi + 32 * yo) * W + xi + 256 * xo] + blur_x[(1 + yi + 32 * yo) * W + xi + 256 * xo] + blur_x[(2 + yi + 32 * yo) * W + xi + 256 * xo]) / ((uint16_t) 3.0);
      }
    }
  }
}
free(blur_x);
}

// tile_and_fused_blur_scheduled(
//     W : size,
//     H : size,
//     blur_y : ui16[H, W] @DRAM,
//     inp : ui16[H + 2, W + 2] @DRAM
// )
void tile_and_fused_blur_scheduled( void *ctxt, int_fast32_t W, int_fast32_t H, uint16_t* blur_y, const uint16_t* inp ) {
EXO_ASSUME(H % 32 == 0);
EXO_ASSUME(W % 256 == 0);
for (int_fast32_t yo = 0; yo < ((H) / (32)); yo++) {
  uint16_t *blur_x = (uint16_t*) malloc(34 * 256 * sizeof(*blur_x));
  for (int_fast32_t xo = 0; xo < ((W) / (256)); xo++) {
    for (int_fast32_t yi = 0; yi < 34; yi++) {
      for (int_fast32_t xi = 0; xi < 256; xi++) {
        blur_x[(yi + 32 * yo - (32 * yo)) * 256 + xi + 256 * xo - (256 * xo)] = (inp[(yi + 32 * yo) * (W + 2) + xi + 256 * xo] + inp[(yi + 32 * yo) * (W + 2) + 1 + xi + 256 * xo] + inp[(yi + 32 * yo) * (W + 2) + 2 + xi + 256 * xo]) / ((uint16_t) 3.0);
      }
    }
    for (int_fast32_t yi = 0; yi < 32; yi++) {
      for (int_fast32_t xi = 0; xi < 256; xi++) {
        blur_y[(yi + 32 * yo) * W + xi + 256 * xo] = (blur_x[(yi + 32 * yo - (32 * yo)) * 256 + xi + 256 * xo - (256 * xo)] + blur_x[(1 + yi + 32 * yo - (32 * yo)) * 256 + xi + 256 * xo - (256 * xo)] + blur_x[(2 + yi + 32 * yo - (32 * yo)) * 256 + xi + 256 * xo - (256 * xo)]) / ((uint16_t) 3.0);
      }
    }
  }
  free(blur_x);
}
}


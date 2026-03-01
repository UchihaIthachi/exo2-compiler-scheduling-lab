from __future__ import annotations

from exo import *
from exo.stdlib.scheduling import *

@proc
def tile_and_fused_blur(
    W: size,
    H: size,
    blur_y: ui16[H, W] @ DRAM,
    inp: ui16[H + 2, W + 2] @ DRAM,
):
    assert H % 32 == 0
    assert W % 256 == 0

    blur_x: ui16[2 + H, W] @ DRAM

    for yo in seq(0, H / 32):
        for xo in seq(0, W / 256):
            for yi in seq(0, 34):
                for xi in seq(0, 256):
                    blur_x[yi + 32 * yo, xi + 256 * xo] = (
                        inp[yi + 32 * yo, xi + 256 * xo]
                        + inp[yi + 32 * yo, 1 + xi + 256 * xo]
                        + inp[yi + 32 * yo, 2 + xi + 256 * xo]
                    ) / 3.0

            for yi in seq(0, 32):
                for xi in seq(0, 256):
                    blur_y[yi + 32 * yo, xi + 256 * xo] = (
                        blur_x[yi + 32 * yo, xi + 256 * xo]
                        + blur_x[1 + yi + 32 * yo, xi + 256 * xo]
                        + blur_x[2 + yi + 32 * yo, xi + 256 * xo]
                    ) / 3.0

def get_loops_at_or_above(cursor):
    """
    Quiz3 fix:
    Include the starting loop (xo) itself; otherwise allocation never sinks
    into xo scope and width cannot shrink to 256.
    """
    loops = [cursor]  # ✅ include cursor
    while not isinstance((parent := cursor.parent()), InvalidCursor):
        loops.append(parent)
        cursor = parent
    return list(reversed(loops))

def schedule(p: Procedure):
    p = rename(p, "tile_and_fused_blur_scheduled")

    xo_loop = p.find_loop("xo")
    producer_alloc = p.find("blur_x : _")

    tile_size = [32, 256]
    blur_x_tile_size = [34, 256]

    loops_to_sink_into = get_loops_at_or_above(xo_loop)

    for i, loop in enumerate(loops_to_sink_into):
        loop = p.forward(loop)
        producer_alloc = p.forward(producer_alloc)

        p = sink_alloc(p, producer_alloc)
        offset_expr = f"{tile_size[i]} * {loop.name()}"
        p = resize_dim(p, producer_alloc, i, blur_x_tile_size[i], offset_expr)

    # share across inner loops in the tile
    p = lift_alloc(p, producer_alloc, 1)
    return p

if __name__ == "__main__":
    w = schedule(tile_and_fused_blur)
    print(w)

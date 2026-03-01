from __future__ import annotations

from exo import *
from exo.stdlib.scheduling import *

@proc
def scaled_add(N: size, a: f32[N], b: f32[N], c: f32[N]):
    assert N % 8 == 0
    for i in seq(0, N):
        c[i] = 2 * a[i] + 3 * b[i]

def stage_exprs(p, num_vectors, assign):
    # helper from quiz2.py
    if isinstance(assign.rhs(), BinaryOpCursor):
        p = bind_expr(p, assign.rhs().lhs(), "vec")
        num_vectors += 1
        p, num_vectors = stage_exprs(p, num_vectors, p.forward(assign).prev())
        p = bind_expr(p, assign.rhs().rhs(), "vec")
        num_vectors += 1
        p, num_vectors = stage_exprs(p, num_vectors, p.forward(assign).prev())
    return p, num_vectors

def schedule(p: Procedure):
    """
    Quiz2 fix:
    Do NOT fission immediately after lifting each allocation (can hide later uses).
    Correct approach: two passes
      (1) expand_dim + lift_alloc for ALL vec temps
      (2) fission after ALL vec assignments
    """
    p = rename(p, "scaled_add_scheduled")
    num_vectors = 0

    p = divide_loop(p, "i", 8, ["io", "ii"], perfect=True)
    p, num_vectors = stage_exprs(p, num_vectors, p.find("c[_] = _"))

    # Pass 1
    for i in range(num_vectors):
        vec_alloc = p.find(f"vec: _ #{i}")
        p = expand_dim(p, vec_alloc, 8, "ii")
        p = lift_alloc(p, vec_alloc)

    # Pass 2
    for i in range(num_vectors):
        vec_assign = p.find(f"vec = _ #{i}")
        p = fission(p, vec_assign.after())

    return p

if __name__ == "__main__":
    w = schedule(scaled_add)
    print(w)

# Dependency Analysis and Scheduling — Exo 2 (Report)

**Task:** In21-S8-CS4553 — Dependency Analysis And Scheduling (Not graded)  
**Paper:** “Exo 2: Growing a Scheduling Language” (Appendix A scheduling primitives)

---

## 1. Semantics vs Scheduling in Exo 2
Exo separates:
- **Semantics / Logic**: the clear reference kernel.
- **Scheduling**: a sequence of verified, semantics-preserving rewrites that target hardware (SIMD, threads, accelerators).

Appendix A lists scheduling primitives grouped into 8 categories.

---

## 2. Step 1 — Appendix A Scheduling Primitive Categories (8)

### A.1 Loop Transformations
**Primitives:** reorder_loops, divide_loop, divide_with_recompute, mult_loops, cut_loop, join_loops, shift_loop, fission, remove_loop, add_loop, unroll_loop  
**Technique:** reshape iteration space (split/tile/interchange/unroll/fission/join).  
**Performance:** enables SIMD-width inner loops, exposes coarse parallel loops (threads), and supports GPU/block-style mapping.

### A.2 Code Rearrangement
**Primitives:** reorder_stmts, commute_expr  
**Technique:** reorder independent statements; commute algebra.  
**Performance:** removes artificial dependencies; improves instruction replacement and vectorization patterns.

### A.3 Scope Transformations
**Primitives:** specialize, fuse, lift_scope  
**Technique:** restructure/move control scopes.  
**Performance:** fusion increases locality; specialization removes overhead when conditions are known; lifting fixes nesting after tiling.

### A.4 Multiple Procedures
**Primitives:** inline, replace, call_eqv, extract_subproc  
**Technique:** inter-procedural scheduling, instruction selection, sub-kernel extraction.  
**Performance:** replace scalar loops with vector intrinsics; swap in optimized equivalent routines; build reusable micro-kernels.

### A.5 Buffer Transformations
**Primitives:** lift_alloc, sink_alloc, delete_buffer, reuse_buffer, resize_dim, expand_dim, rearrange_dim, divide_dim, mult_dim, unroll_buffer, bind_expr, stage_mem  
**Technique:** move allocations, change shapes/layout, stage windows into temps.  
**Performance:** cache/shared-memory style tiling (stage_mem); register tiling (expand/divide); smaller footprints (sink+resize); reuse buffers across non-overlapping lifetimes.

### A.6 Simplification
**Primitives:** simplify, eliminate_dead_code, rewrite_expr, merge_writes, inline_window, inline_assign  
**Technique:** clean up overhead from prior transforms.  
**Performance:** fewer redundant loads/stores/writes; tighter generated code.

### A.7 Backend-Checked Annotations
**Primitives:** set_memory, set_precision, parallelize_loop, set_window  
**Technique:** add annotations checked by backend/codegen.  
**Performance:** makes intrinsics matching memory-aware; ensures loops are safe to parallelize; preserves ABI/precision correctness.

### A.8 Configuration State
**Primitives:** bind_config, delete_config, write_config  
**Technique:** schedule configuration writes to stateful accelerators.  
**Performance:** hoist/remove redundant config updates to reduce overhead.

---

## 3. Step 2 — Install Exo and run examples

### Install (pip)
pip install exo-lang

### Or build from source
git clone https://github.com/exo-lang/exo.git
cd exo
git submodule update --init --recursive
python -m venv ~/.venv/exo
source ~/.venv/exo/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
python -m build .
pip install dist/*.whl

Run quizzes:
- exo/examples/quiz1: exocc quiz1.py
- exo/examples/quiz2: exocc quiz2.py
- exo/examples/quiz3: exocc quiz3.py

---

## 4. Step 3 — Quizzes (issues + correct/incorrect)

### Quiz 1 — AVX2 replacement not happening
**Issue:** schedule looks “vector-shaped”, but intrinsics not used.  
**Incorrect:** calling replace_all before setting memory types.  
**Correct:** set_memory(..., AVX2) on staged buffers before replace_all.  
**Solution:** solutions/quiz1_solution.py

### Quiz 2 — SchedulingError on fission
**Issue:** fission would hide a temporary allocation from later use.  
**Incorrect:** expand_dim + lift_alloc + fission immediately per temp.  
**Correct:** 2-pass schedule (lift all allocs first, then fission assigns).  
**Solution:** solutions/quiz2_solution.py

### Quiz 3 — blur_x width not shrinking to 256
**Issue:** helper omitted xo loop so allocation never sunk into xo scope.  
**Incorrect:** loops=[] and only parents collected.  
**Correct:** loops=[cursor] to include xo loop.  
**Solution:** solutions/quiz3_solution.py

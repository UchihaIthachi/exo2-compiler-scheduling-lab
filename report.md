# Dependency Analysis and Scheduling — Exo 2 (Report)

**Task:** In21-S8-CS4553 — Dependency Analysis And Scheduling (Not graded)  
**Paper Focus:** “Exo 2: Growing a Scheduling Language” (Appendix A scheduling primitives)

---

## 1. The Separation of Semantics and Scheduling in Exo 2

Usually, compilers aggressively optimize source code. If a target architecture has specific features such as vector extensions or custom accelerators, a traditional compiler often re-organizes the source code to utilize these extensions under the hood without changing the semantics of the program. However, ensuring high performance often requires intricate tuning that standard compilers struggle to safely automate.

Exo 2 is a domain-specific scheduling language that decouples these two aspects into distinct components:
1. **Semantics / Logic:** The clean, reference kernel representing the fundamental algorithm.
2. **Scheduling:** A sequence of user-defined, verified, and semantics-preserving rewrites that target specific hardware performance characteristics (e.g., SIMD, multithreading).

By doing this, engineers can iterate aggressively on performance without risking the fundamental correctness of the algorithmic semantics. 

Appendix A of the Exo 2 paper classifies scheduling primitives into 8 distinct categories, each designed to manipulate loops, memory, and procedure calls safely.

---

## 2. Step 1 — Scheduling Primitive Categories (Appendix A)

### A.1 Loop Transformations
**Primitives:** `reorder_loops`, `divide_loop`, `divide_with_recompute`, `mult_loops`, `cut_loop`, `join_loops`, `shift_loop`, `fission`, `remove_loop`, `add_loop`, `unroll_loop`  
**Technique:** The goal is to reshape the overall iteration space by safely splitting, tiling, interchanging, unrolling, separating (fission), or merging (join) loops.  
**Performance Gain:** This shapes the loops to map efficiently onto specific hardware topologies. It naturally uncovers SIMD-width data streams for the innermost loops, exposes coarse thread-level parallelism via parallelized outer loops (pthreads), and supports complex blocking strategies suited for GPU memory hierarchies.

### A.2 Code Rearrangement
**Primitives:** `reorder_stmts`, `commute_expr`  
**Technique:** Rearranging independent mathematical statements or leveraging algebraic commutativity rules.  
**Performance Gain:** This effectively mitigates artificial data dependencies. By shifting instructions, compilers can form denser patterns suitable for instruction replacement or advanced vectorization schemas.

### A.3 Scope Transformations
**Primitives:** `specialize`, `fuse`, `lift_scope`  
**Technique:** Restructuring or relocating entire control scopes safely.  
**Performance Gain:** Scope fusion significantly increases cache locality. Specialization eradicates redundant conditional checks by resolving overhead at compile time when specific constraints are mathematically proven. Scope lifting resolves complex nesting structures introduced post-tiling operations.

### A.4 Multiple Procedures
**Primitives:** `inline`, `replace`, `call_eqv`, `extract_subproc`  
**Technique:** Executing inter-procedural optimizations, custom instruction selection mappings, or isolating specific algorithm subsets into sub-kernels.  
**Performance Gain:** The key component of micro-kernel design, this allows developers to systematically replace slow scalar loops with heavily optimized hardware vector intrinsics (such as AVX2). Furthermore, it allows substituting equivalent routines while ensuring complete semantic parity.

### A.5 Buffer Transformations
**Primitives:** `lift_alloc`, `sink_alloc`, `delete_buffer`, `reuse_buffer`, `resize_dim`, `expand_dim`, `rearrange_dim`, `divide_dim`, `mult_dim`, `unroll_buffer`, `bind_expr`, `stage_mem`  
**Technique:** Modifying buffer allocation locations, altering underlying dimensionality, shapes, or data layouts, and staging memory windows directly into hardware temporary registers.  
**Performance Gain:** Critical for enforcing strict cache and shared-memory tiling behaviors (via `stage_mem`). It ensures arrays fit perfectly within constrained register spaces (`expand` or `divide`). Decreases the general application memory footprint (`sink` combined with `resize`) and drastically improves efficiency by guaranteeing the reuse of buffers across distinct operational lifetimes.

### A.6 Simplification
**Primitives:** `simplify`, `eliminate_dead_code`, `rewrite_expr`, `merge_writes`, `inline_window`, `inline_assign`  
**Technique:** Streamlining loops to clean up excessive overhead generated strictly from the preceding transformation steps.  
**Performance Gain:** Results in tighter, streamlined generated code. It directly eradicates structurally redundant loads, duplicate writes, or dead-code paths.

### A.7 Backend-Checked Annotations
**Primitives:** `set_memory`, `set_precision`, `parallelize_loop`, `set_window`  
**Technique:** Explicitly adding precise data annotations that the backend compiler code generator natively verifies.  
**Performance Gain:** It actively guarantees that loops selected for multi-threading are strictly memory-safe for parallel execution. The annotations are also essential for forcing specific SIMD intrinsics, correctly aligning precision types, and guaranteeing strict hardware ABI correctness.

### A.8 Configuration State
**Primitives:** `bind_config`, `delete_config`, `write_config`  
**Technique:** Directly scheduling the underlying configuration state writes strictly geared toward stateful hardware accelerators.  
**Performance Gain:** Heavily reduces structural state overhead by successfully hoisting out generic configuration setup phases and eliminating duplicated or redundant state writes occurring entirely within the innermost hardware loop limits.

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

## 4. Step 3 — Quiz Scenarios and Solutions

The following are descriptions of the issues encountered in the provided scheduling quizzes, along with analyses of the incorrect approaches and the verified, correct solutions.

### Quiz 1 — AVX2 Replacement Not Occurring
**Issue:** The generated schedule correctly mimics the structure of SIMD vector code but fails to invoke the underlying hardware vector intrinsics. It is still executing scalar operations one element at a time.
**Incorrect Approach:** Invoking the `replace_all(p, avx_instrs)` schedule directive *before* correctly defining the memory topology of the target staged buffers.
**Correct Solution:** The `replace_all` function in Exo is memory-aware. Therefore, you must invoke `set_memory(p, f"{name}_vec", AVX2)` on all intermediate buffer arrays before performing the replacement. Once the memory context is explicitly `AVX2`, the compiler pattern-matches and replaces the statements with the correct `_mm256_*` intrinsic mappings.
**Source:** `solutions/quiz1_solution.py`

### Quiz 2 — SchedulingError During Loop Fission
**Issue:** The compiler throws a `SchedulingError` stating "Will not fission here, because doing so will hide the allocation of vec from a later use site."
**Incorrect Approach:** Utilizing a single loop iteration to immediately perform `expand_dim`, `lift_alloc`, and `fission` sequentially for each temporary array. This hides the earlier allocations from subsequent uses because the memory allocations remain trapped within the split loop bodies.
**Correct Solution:** Refactoring the scheduling code to operate in a 2-pass schema. First, loop over the structures and run `expand_dim` and `lift_alloc` on all temporary allocations to safely hoist them outside the computation context. Secondly, safely run a subsequent loop to `fission` the individual assignment operations. 
**Source:** `solutions/quiz2_solution.py`

### Quiz 3 — `blur_x` Width Fails to Shrink
**Issue:** While attempting to tile a blur operation, the scheduler successfully shrinks the overall allocation height dimension to 34 but entirely fails to dynamically reduce the width mapping down to 256. 
**Incorrect Approach:** The helper function `get_loops_at_or_above(cursor)` initializes its traversal collection as `loops = []`. This fundamentally omits the initial underlying cursor (the innermost `xo` loop). Consequently, the intermediate array allocation is never sunk deep enough into the `xo` scope.
**Correct Solution:** Modifying the initialization definition to `loops = [cursor]` correctly captures the `xo` loop mapping inside the traversal collection. This allows the allocation to gracefully sink into the correct inner tile representation, reducing the active layout requirements perfectly down to `[34, 256]`.
**Source:** `solutions/quiz3_solution.py`

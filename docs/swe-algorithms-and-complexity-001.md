# SWE algorithms-and-complexity coverage slice 001

This slice is the first competency-driven population pass under `coverage/swe.yaml`.

## Baseline

Before this slice, the SWE coverage validator reported `algorithms-and-complexity` at D1=1, D2=4 and D3=2. Existing questions already covered interval merging, binary-search debugging, streaming top-k, dependency ordering/cycle diagnostics and general Big O.

## Added foundation coverage

Ten native D1 questions add distinct foundations rather than surface variations:

- best/average/worst-case analysis
- space and auxiliary-space complexity
- binary-search preconditions and invariants
- BFS versus DFS
- recursion, termination and call-stack behaviour
- stable sorting
- greedy versus dynamic-programming strategy
- amortised complexity
- divide-and-conquer
- algorithm invariants and correctness reasoning

## Added application/depth coverage

- `tic-q-000046` applies graph traversal to an unweighted grid shortest-path problem at D2.
- `tic-q-000047` applies sorting and space-complexity fundamentals to external sorting under memory, I/O and restart constraints at D3.

The goal is not to close the competency permanently. Coverage floors are minimum planning signals, not caps; future non-duplicative algorithm questions remain welcome at any appropriate difficulty.

## Progression

`paths/swe.yaml` now links foundational nodes to existing and new questions using escalation/recovery edges. Not every D1 has a forced descendant. Some concepts can remain useful standalone probes until a genuinely valuable higher-demand assessment exists.

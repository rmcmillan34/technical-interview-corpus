# SWE data-structures coverage slice 001

This is the second competency-driven population pass under `coverage/swe.yaml`.

## Baseline

Before this slice, the coverage validator reported `data-structures` at D1=4, D2=4 and D3=2. Much of the D1 count came from secondary classification on algorithm questions rather than dedicated data-structure fundamentals. Existing application/depth questions already include the parameterised LRU cache, streaming top-k, graph traversal, and the TTL+LRU production cache.

## Added foundation coverage

Six native D1 questions add primary coverage for:

- arrays versus linked lists
- stacks versus queues
- hash tables, collisions and load factor
- binary trees versus binary search trees
- heaps and priority queues
- adjacency-list versus adjacency-matrix graph representation

## Added application/depth coverage

- `tic-q-000054` implements a min-stack with constant-time minimum queries at D2.
- `tic-q-000055` designs a large in-memory timer scheduler index with priority ordering, direct identity lookup, cancellation/rescheduling, stale-state cleanup and deterministic testing at D3.

Together with existing records, the slice is intended to move data-structures above the core D1/D2/D3 planning floors without manufacturing D4 or D5 content.

## Progression

The SWE progression graph connects the new foundations to existing LRU, top-k, graph and cache assessments and to the new min-stack/timer-scheduler questions. Standalone foundations remain valid even when no higher-level descendant adds useful assessment value yet.

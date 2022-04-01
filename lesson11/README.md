My implementation of the [brili](https://github.com/sampsyo/bril/tree/main/bril-ts) interpreter with Reference Counting Garbage Collection.

## RCGC
The reference count garbage collector (`ReferenceCountGarbargeCollector`) is used by `brili.ts` in the following ways
* On an `alloc` the count for that object is initialized with a count of 1.
* On a call to a function, increment all object reference counts. After the function returns, decrement all object reference counts.
* On a pointer addition, decrement the destination pointer's previous object reference count. Then increment the new object's reference count.
* On a function returning a pointer, initialize a new reference counter for a new object.
* On an `id` of a pointer, do something similar to pointer addition book-keeping.

As with reference counting, once a reference is decremented to 0, the object is first checked if it points to a reference, which is then decremented. I want to test this more, but as of now it passes the simple test case of `ptrrrecurse.bril`.

## Testing
For testing, I took the benchmarks which explicitly have memory operations, and either removed the free instructions (in `benchmarks-mem`) or kept them (in `benchmarks-gc`). This produced the correct results using turnt, so that's pretty good.

One thing I missed when initially implementing my garbage collector was removing references at the end of main. It seems like most of the benchmarks declare references in main, and the only time they can be removed is at the end of main. This led to some initial confusion, but it was pretty easy to debug.
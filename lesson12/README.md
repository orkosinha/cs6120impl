My implementation of the modified [brili](https://github.com/orkosinha/cs6120impl/tree/main/lesson12) interpreter with tracing.

## Tracing
Tracing is implemented starting from the main function to the first `call`, `print`, `store`, `alloc`, or `free` as a starting point. I construct the trace with the modified interpreter in the first run, add it to the program and run it through the non-modified interpreter. 

Some specifications to my [`trace` function](https://github.com/orkosinha/cs6120impl/blob/1b7169d2e8c3d695e54c64c62a8212610ac54cd2/lesson12/brilitc.ts#L410)

* I need to bail out of edges that contain things I can't support. Basically just set an always false guard in those scenarios.
* I need to invert the value of branch conditions so guards are not triggered to bail out unnecessarily.
* If a jmp has been encountered before while tracing, then I should commit and end tracing.

## Results
The results were not impressive, probably the opposite as nothing really got any performance improvements. However, the way tracing is implemented here, it makes sense as it's only from the main function with no optimizations performed on the trace.

Here are the results from the benchmarks, thankfully nothing crashed and the same results were produced. So, it's a very slight success in that I am adding code and getting the same results. I thought it was interesting that the pow benchmark gained a 25% of it's original instruction count.
| Benchmark                  | Percent Change |
| -------------------------- | -------------- |
| mat-mul                    | 0.00%          |
| ackermann                  | 0.00%          |
| catalan                    | 0.00%          |
| eight-queens               | 0.00%          |
| primes-between             | 0.00%          |
| adj2csr                    | 0.01%          |
| pythagorean\_triple        | 0.01%          |
| adler32                    | 0.06%          |
| sieve                      | 0.09%          |
| orders                     | 0.09%          |
| check-primes               | 0.12%          |
| sum-sq-diff                | 0.13%          |
| cholesky                   | 0.16%          |
| relative-primes            | 0.31%          |
| quadratic                  | 0.38%          |
| mat-inv                    | 0.48%          |
| sqrt                       | 0.62%          |
| n\_root                    | 0.68%          |
| fizz-buzz                  | 0.96%          |
| bubblesort                 | 1.19%          |
| up-arrow                   | 1.19%          |
| perfect                    | 1.29%          |
| max-subarray               | 1.55%          |
| euclid                     | 1.60%          |
| loopfact                   | 1.72%          |
| riemann                    | 2.01%          |
| digital-root               | 2.43%          |
| binary-fmt                 | 3.00%          |
| collatz                    | 3.55%          |
| newton                     | 3.69%          |
| pascals-row                | 4.11%          |
| gcd                        | 4.35%          |
| armstrong                  | 4.51%          |
| recfact                    | 4.81%          |
| fib                        | 4.96%          |
| sum-divisors               | 10.06%         |
| sum-bits                   | 12.33%         |
| binary-search              | 15.38%         |
| ray-sphere-intersection    | 16.20%         |
| factors                    | 18.06%         |
| rectangles-area-difference | 21.43%         |
| pow                        | 25.00%         |
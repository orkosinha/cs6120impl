import {Ident} from './bril'
import {Pointer, Value, Env, Heap, Key} from './briligc'

// adh2csr.bril
// adler32.bril
// binary-search.bril
// bubblesort.bril
// cholesky.bril
// eight-queen.bril
// fib.bril
// mat-inv.bril
// mat-mul.bril
// max-subarray.bril
// sieve.bril

export class ReferenceCountGarbageCollector {
  heap: Heap<Value>;
  count: Map<number, number>;
  constructor (heap: Heap<Value>) {
    this.heap = heap;
    this.count = new Map();
  }
  
  new(obj: Key): void {
    this.count.set(obj.base, 1);
  }

  dec(obj: Key): void {
    let count: number | undefined = this.count.get(obj.base);
    if (count) {
      if (count - 1 == 0) {
        let value: Value = this.heap.read(obj);
        if (value.hasOwnProperty('loc')) {
          this.dec((value as Pointer).loc);
        }
        this.count.delete(obj.base);
        this.heap.free(new Key(obj.base, 0));
      }
      this.count.set(obj.base, count - 1);
    }
  }

  inc(obj: Key): void {
    let count: number | undefined = this.count.get(obj.base);
    if (count) {
      this.count.set(obj.base, count + 1);
    }
  }

  incEnv(env: Env): void {
    env.forEach((v, d) => {
      // if ((v as Pointer).type) {
      if (v.hasOwnProperty('loc')) {
        this.inc((v as Pointer).loc);
      }
    });
  }

  decEnv(env: Env): void {
    env.forEach((v, d) => {
      // if ((v as Pointer).type) {
      if (v.hasOwnProperty('loc')) {
        this.dec((v as Pointer).loc);
      }
    });
  }

  assign(dest: Ident, env: Env, obj: Key): void {
    let value: Value | undefined = env.get(dest);
    if (value && value.hasOwnProperty('loc')) {
      let ptr: Pointer = value as Pointer;
      this.dec(ptr.loc);
    }
    this.inc(obj);
  }
}
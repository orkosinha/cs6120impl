# Lesson 3: Local Analysis & Optimization

This is an implementation of the tasks from [here](https://www.cs.cornell.edu/courses/cs6120/2022sp/lesson/3/#tasks).

## Usage
```
usage: lesson3.py [-h] [-l] [-d]

options:
  -h, --help  show this help message and exit
  -l, --lvn   perform optimizations using local value numbering and pass of dce
  -d, --dce   perform trivial dead code elimination optimization and dce pass
```

In the context of other bril tools, I use `bril2json < ./tests/lvn01.bril | ./lesson3.py -o | bril2txt` to get the more readable versions of bril programs.

## Dead Code Elimination
Trivial dead code elimination is implemented from the pseudocode in class.

The pseudocode discussed in class was very straight forward.

## Local Value Numbering
Local value numbering is implemented with CSE exploiting commutativity and copy propogation.

I originially started by trying to follow the pseudocode as closely as possible, but it wasn't that simple. The first problem I ran into was the control flow of when to assign a new number and when to lookup in the table due to the variety of operations.

Variables that were declared before the block but used in the current block proved to be an issue. I took care of this by assigning a lvn number to these previously declared variables. 

Another major issue I ran into was handling re-defined variables. I used the following example discussed in class
```
@main {
    a: int = const 1;
    b: int = const 2;
    c: int = const 3;
    d: int = const 4;
    x: int = add a b;
    x: int = mul c d;
    y: int = add a b;
    print y;
}
```
I originally renamed the variable and wanted to rename all occurences before the next assignment to the new name, but it was simpler to just add it to my `var2num` map. Eventually, this will get overwritten by the redefinition, so it seemed okay to do.

## Testing
I tested my optimizations using the `./tests/` directory and Turnt. Most of the tests are from the examples in class, but I also cherry-picked some of the benchmarks using core Bril and tested with Turnt. 


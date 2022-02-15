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


## Local Value Numbering

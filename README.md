# Problem Statement

There is a large file (potentially larger than 10G) that
contains lines of text. We have to write a program that
reads data from that input file and creates two output
files as follows:

  - OutputFile1: Each line prints line number with
    total word count for that line.

  - OutputFile2: All unique words (case insensitive) in the
    input file and its count, one pair per line.

## Example

### Input
```
Two roads diverged in a yellow wood
And sorry I could not travel both
And be one traveler long I stood
And looked down one as far as I could
To where it bent in the undergrowth
```

### Output
#### OutputFile1
```
1 7
2 7
3 7
4 9
5 7
```
#### OutputFile1
```
two 1
roads 1
diverged 1
in 2
a 1
yellow 1
wood 1
and 3
sorry 1
i 3
could 2
not 1
travel 1
both 1
be 1
one 2
traveler 1
long 1
stood 1
looked 1
down 1
as 2
far 1
to 1
where 1
it 1
bent 1
the 1
undergrowth 1
```

# Solutions

## Simple Solutions
A simple C++ solution is `cpp/wordslines.cpp`.
The following steps builds the C++ executable at `cpp/build/wordslines`.
```
$ cd cpp
$ mkdir -p build
$ cd build
$ ../build.sh
```

A simple Python3 solution is `python/wordslines.py`.

## Better Solutions

How can we improve upon the simple solution?

`TO-BE-PUBLISHED`

# Verification

## Input File Generation
There is a `.go` file to generate an input text file
of the (approximate) specified size.

```
$ cd generator

$ go run generate_file.go 100000
Creating input file...
$

$ ls -l inputfile 
-rw-r--r-- 1 arun arun 100024 Nov 18 16:06 inputfile
$ 
```

## Comparative Verification

`verifier/verifier.py` is a simple verifier. It takes
two arguments, namely:

 - the input file to verify with, and

 - the executable file (C++, Python, Go) to verify.

The verifier computes the lines and words properties
of the provided input file using the standard Unix
programs like, `wc`, `sort`, `tr`, etc.

Then it runs the executable with that input file.

Finally, it compares the observed output of the
executable with the expected output computed earlier.

Here is a sample verification of the C++ executable.
```
$ python3 verifier.py ../generator/inputfile ../cpp/build/wordslines 
Using file ../generator/inputfile to verify exe ../cpp/build/wordslines
Verification successful!
$
```

Here is a sample verification of the Python3 solution.
```
$ python3 verifier.py ../generator/inputfile ../python/wordslines.py 
Using file ../generator/inputfile to verify exe ../python/wordslines.py
Verification successful!
$ 
```




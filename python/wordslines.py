#!/usr/bin/env python3

import sys
from collections import defaultdict

class Result:
    def __init__(self, words_at_line, word_count):
        self.words_at_line = words_at_line
        self.word_count = word_count


def VanillaSolution(infname):
    with open(infname, 'r') as f:
        lines = [line.strip() for line in f]

    nlines = len(lines)
    words_at_line = [0] * nlines
    word_count = defaultdict(int)

    for idx, line in enumerate(lines):
        line = str(line)
        words = line.split()
        words_at_line[idx] = len(words)
        for word in words:
            word = word.lower()
            word_count[word] += 1

    return Result(words_at_line, word_count)


def WriteResult(result, out1fname, out2fname):
    with open(out1fname, 'w') as f:
        for idx, wordcount in enumerate(result.words_at_line):
            line = f"{idx+1} {wordcount}\n"
            f.write(line)

    with open(out2fname, 'w') as f:
        for word, count, in result.word_count.items():
            line = f"{word} {count}\n"
            f.write(line)


def main():
    if len(sys.argv) < 4:
        print(f"usage: {sys.argv[0]} <input-filename> <output-filename-1> <output-filename-2>")
        return

    infname, out1fname, out2fname = sys.argv[1], sys.argv[2], sys.argv[3]

    result = VanillaSolution(infname)
    WriteResult(result, out1fname, out2fname)

if __name__ == "__main__":
    main()

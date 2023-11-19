import subprocess
import sys
import os
from timeit import default_timer as timer

# Run 'wc' on infilename and return the (lines, words).
def wc(infilename):
    stdout_bytes = subprocess.check_output(['wc', infilename])
    stdout_string = stdout_bytes.decode("utf-8")
    stdout_parts = stdout_string.split()
    lines, words, chars = int(stdout_parts[0]), int(stdout_parts[1]), int(stdout_parts[2])
    return lines, words, chars


# Return list of (word, count) sorted by word from arbitrary infilename.
# The words are transformed to lowercase.
def expectedWordCounts(infilename):
    templowerfilename = "/tmp/lowerfilename280492380"
    command1 = f"tr '[:upper:]' '[:lower:]' < {infilename} > {templowerfilename}"
    os.system(command1)

    insortedfilename = "/tmp/insortedfilename1391124"
    command2 = f"tr -s '[[:punct:][:space:]]' '\n' < {templowerfilename} | sort | uniq -c | sort -k 1 > {insortedfilename}"
    os.system(command2)

    with open(insortedfilename, 'r') as f:
        lines = [line.strip() for line in f]
    word_counts = []
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            continue
        freq, word = int(parts[0]), str(parts[1])
        word_counts.append((word, freq))
    word_counts.sort()
    return word_counts


# Return list of (word, count) sorted by word from formatted outfilename2.
def observedWordCounts(outfilename2):
    with open(outfilename2, 'r') as f:
        lines = [line.strip() for line in f]
    word_counts = []
    for line in lines:
        parts = line.split()
        word, freq = str(parts[0]), int(parts[1])
        word_counts.append((word, freq))
    word_counts.sort()
    return word_counts


def execute(exe, infilename, outfilename1, outfilename2):
    subprocess.call([exe, infilename, outfilename1, outfilename2])


# Return (num-lines, line-count-sum) in outfilename1.
def count_lineswords(outfilename1):
    with open(outfilename1, 'r') as f:
        lines = [line.strip() for line in f]
    expected_lineno = 1
    count_sum = 0
    for line in lines:
        parts = line.split()
        lineno, count = int(parts[0]), int(parts[1])
        if lineno != expected_lineno:
            assert False, f"{lineno}, {count}"
        expected_lineno += 1
        count_sum += count
    return len(lines), count_sum


def verify(nlines, nwords, expected_word_counts, infilename, outfilename1, outfilename2):
    observed_lines, observed_word_count = count_lineswords(outfilename1)
    assert observed_lines == nlines, f"observed lines {observed_lines} != expected {nlines}"
    assert observed_word_count == nwords, f"observed word count {observed_word_count} != expected {nwords}"

    observed_word_counts = observedWordCounts(outfilename2)
    assert observed_word_counts == expected_word_counts, f"observed word counts {observed_word_counts} != expected word counts {expected_word_counts}"

    print(f"OK")


def main():
    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} <path-to-input-file> <path-to-executable>")
        return

    infilename = sys.argv[1]
    exe = sys.argv[2]

    nlines, nwords, nchars = wc(infilename)
    print(f"Input file = {infilename} ({nchars} bytes), program = {exe}")
    expected_word_counts = expectedWordCounts(infilename)

    out1, out2 = "out1.out", "out2.out"
    start = timer()
    execute(exe, infilename, out1, out2)
    end = timer()

    verify(nlines, nwords, expected_word_counts, infilename, out1, out2)

    delta_seconds = end - start
    delta_microseconds = delta_seconds * 1000 * 1000
    print(f"Time = {delta_microseconds:.0f} us")


if __name__ == "__main__":
    main()



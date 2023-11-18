package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

// Number of words used for generation.
const N = 15

var words [N]string = [N]string{
	"road",
	"wood",
	"yellow",
	"where",
	"looked",
	"travel",
	"cat",
	"mouse",
	"water",
	"sky",
	"dog",
	"bird",
	"cheese",
}

// Generate lines and keep sending to the channel forever.
func generateLines(send chan []string) {
	// Maximum words in a line.
	const L = 7

	s := rand.New(rand.NewSource(31428))
	r1 := rand.New(s)

	for {
		n := r1.Int31n(L)
		line := make([]string, n)
		for i := int32(0); i < n; i++ {
			randWordIdx := r1.Int31n(N)
			line = append(line, words[randWordIdx])
		}
		send <- line
	}
}

func main() {
	var fileSize int = 10000000000
	if len(os.Args) > 1 {
		fileSize, _ = strconv.Atoi(os.Args[1])
	}

	fmt.Printf("Creating input file...")
	file, err := os.Create("inputfile")
	if err != nil {
		panic("failed to create input file")
	}
	defer file.Close()

	// Create a buffered channel of string slices.
	bufSize := 1024 * 1024
	chanSend := make(chan []string, bufSize)

	// Use multiple concurrent workers.
	workers := 8
	for i := 0; i < workers; i++ {
		go generateLines(chanSend)
	}

	ticker := time.NewTicker(20 * time.Second)
	w := bufio.NewWriterSize(file, bufSize)

	run := true
	total := 0
	for run {
		select {
		case row, ok := <-chanSend:
			if !ok {
				break
			}
			if len(row) == 0 {
				continue
			}
			line := strings.Join(row, " ")
			line = line + "\n"
			if w.Available() < len(line) {
				err := w.Flush()
				if err != nil {
					panic("flush error")
				}
			}
			size, err := w.WriteString(line)
			if err != nil {
				panic("write error")
			}
			total += size
			if total > fileSize {
				run = false
				break
			}

		case <-ticker.C:
		}
	}
	w.Flush()
}

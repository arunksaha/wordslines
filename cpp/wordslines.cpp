#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>

using namespace std;

typedef int32_t LineCounter;
typedef vector<LineCounter> WordsAtLine;
typedef int32_t WordCounter;
typedef unordered_map<string, WordCounter> WordCounterMap;


struct Result {
  // words_at_line_[i] = number of words in line i.
  WordsAtLine words_at_line_;

  // Map: word -> count.
  WordCounterMap word_count_;
};


Result
VanillaSolution(ifstream & ifs) {
  Result result;
  vector<string> words;
  istringstream iss;
  for (string line; getline(ifs, line); ) {
    iss.clear();
    iss.str(line);
    words.assign(istream_iterator<string>{iss}, istream_iterator<string>{});
    result.words_at_line_.push_back(static_cast<LineCounter>(words.size()));
    for (auto & word : words) {
      transform(begin(word), end(word), begin(word), ::tolower);
      result.word_count_[word] += 1;
    }
  }
  return result;
}


void
WriteResult(Result const& result, ostream & os1, ostream & os2) {
  for (size_t i = 0; i < result.words_at_line_.size(); ++i) {
    os1 << i+1 << ' ' << static_cast<int>(result.words_at_line_[i]) << '\n';
  }
  for (auto const& kv : result.word_count_) {
    os2 << kv.first << ' ' << kv.second << '\n';
  }
}


int main(int argc, char * argv[]) {
  if (argc < 4) {
    cerr << "Usage: " << argv[0] << " <input-filename> <output-filename-1> <output-filename-2>\n";
    return 0;
  }
  char const * const filename = argv[1];
  ifstream ifs{filename, ios::binary};
  if (!ifs.is_open()) {
    cerr << "Failed to open file " << filename << '\n';
    return 0;
  }

  char const * const output_filename_1 = argv[2];
  char const * const output_filename_2 = argv[3];
  
  Result const result_vanilla = VanillaSolution(ifs);
  ofstream ofs1{output_filename_1};
  ofstream ofs2{output_filename_2};
  WriteResult(result_vanilla, ofs1, ofs2);
}

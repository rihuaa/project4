from hashtables import *
import math
import os
import sys

class SearchEngine:
    def __init__(self, directory, stopwords):
        # Replace HashMap() with your hash table.
        self.doc_length = HashTableLinear() # The key is filename, the value is the number of words
        self.term_freqs = HashTableLinear() # The key is word, the value is another HashMap
        self.stopwords = stopwords
        self.index_files(directory)

    def __eq__(self, other):
        return isinstance(other, SearchEngine) \
        and self.doc_length == other.doc_length \
        and self.term_freqs == other.term_freqs \
        and self.stopwords == other.stopwords \
        and self.index_files == other.index_files

    def __repr__(self):
        return "SearchEngine({}, {}, {}, {})".format(self.doc_length, \
        self.term_freqs, self.stopwords, self.index_files)

    def read_file(self, infile):
        """A helper function to read a file
        Args:
        infile (str) : the path to a file
        Returns:
        list : a list of str read from a file
        """
        lines = []
        with open(infile) as input_file:
            for line in input_file:
                lines.append(line)
            # lines = input_file.readlines()
        return lines

    def parse_words(self, lines):
        """split strings into words
        Convert words to lower cases and remove new line chars.
        Exclude stopwords.
        Args:
        lines (list) : a list of strings
        Returns:
        list : a list of words
        """
        words = []
        for line in lines:
            for word in line.split():
                if word not in self.stopwords:
                    words.append(word.lower())
        return words

    def count_words(self, filename, words):
        """count words in a file and store the frequency of each
        word in the term_freqs hash table. The keys of the term_freqs hash
        table shall be words.
        The values of the term_freqs hash table shall be hash tables (term_freqs
        is a hash table of hash tables). The keys of the hash tables (inner hash
        table) stored in the term_freqs shall be file names.
        The values of the inner hash tables shall be the frequencies of words.
        For example, self.term_freqs[word][filename] += 1;
        Words should not contain stopwords.
        Also store the total count of words contained in the file in the doc_length hash table.
        Args:
        filename (str) : the file name
        words (list) : a list of words
        """
        self.doc_length.put(filename, 0)
        for word in words:
            if word in self.term_freqs:
                if filename in self.term_freqs[word]:
                    self.term_freqs[word][filename] += 1
                else:
                    self.term_freqs[word][filename] = 1
            else:
                self.term_freqs.put(word, HashTableLinear())
                self.term_freqs[word][filename] = 1
            self.doc_length[filename] += 1

    def index_files(self, directory):
        """index all text files in a given directory
        Args:
        directory (str) : the path of a directory
        """
        files = os.listdir(directory)
        for file in files:
            path = os.path.join(directory, file)
            if os.path.isfile(path):
                root_ext = os.path.splitext(file)
                if root_ext[1] == '.txt':
                    word_list = self.parse_words(self.read_file(path))
                    self.count_words(path, word_list)

    def get_wf(self, tf):
        """computes the weighted frequency
            Args:
            tf (float) : term frequency
            Returns:
            float : the weighted frequency
        """
        if tf > 0:
            wf = 1 + math.log(tf)
        else:
            wf = 0
        return wf

    def get_scores(self, terms):
        """creates a list of scores for each file in corpus
        The score = weighted frequency / the total word count in the file.
        Compute this score for each term in a query and sum all the scores.
        Args:
            terms (list) : a list of str
        Returns:
            list : a list of tuples, each containing the filename and its relevancy score
        """
        # create scores hashmap
        # for each query term t
        #   fetch a hash table of t from self.term_freqs
        #   for each file in the hash table, add wf to scores[file]
        # for each file in scores, do scores[file] /= self.doc_length[file]
        # return scores
        scores = HashTableLinear()
        for term in terms:
            files_for_term = self.term_freqs[term] # gets table of directories
            # print(files_for_term)
            # print(type(files_for_term))
            file_paths = files_for_term.keys() # gets list of path names
            # print('file path', file_paths)
            # print('file path type', type(file_paths))
            for file in file_paths: # file is path name(key)
                score = self.get_wf(self.term_freqs[term][file])
                # print(score)
                # print(file)
                if file in scores:
                    scores[file] += score
                else:
                    scores.put(file, score)
        dirs = scores.keys()
        file_score = []
        # print(dirs)
        for dir in dirs:
            scores[dir] /= self.doc_length[dir]
            file_score.append((dir, scores[dir]))
        # print(file_score)
        return file_score

    def rank(self, scores):
        """ranks files in the descending order of relevancy
        Args:
            scores (list) : a list of tuples: (filename, score)
        Returns:
            list: a list of tuples: (filename, score) sorted in descending
            order of relevancy
        """
        if len(scores) == 1:
            return scores
        return insertion_sort(scores)

    def search(self, query):
        """ search for the query terms in files
            Args:
                query (str) : query input
            Returns:
                list : list of files in descending order or relevancy
        """
        query = query.split()
        words = self.parse_words(query)
        table = HashTableLinear()
        for word in words:
            table.put(word, word)
        keys = table.keys()
        # print(keys)
        file_score = self.get_scores(keys) # (filename, score) tuple
        res = self.rank(file_score)
        return res

def insertion_sort(alist):
    """Takes a tuple of string, int pairs and performs insertion sort
    based on int in descending order.

    Args:
        alist (list): a list of integers

    Returns:
        int: the number of comparisons performed in the sort
    """
    size = len(alist)
    print(alist)
    for i in range(1, size):
        j = i
        while j > 0 and alist[j - 1][1] > alist[j][1]:
            print('alist[j - 1][1]\t', alist[j - 1][1])
            print('alist[j][1]\t', alist[j][1])
            alist[j - 1][0], alist[j][0] = alist[j][0], alist[j - 1][0]
            alist[j - 1][1], alist[j][1] = alist[j][1], alist[j - 1][1]
            j = j - 1
    return alist[::-1]

if __name__ == '__main__':
    stopwords = import_stopwords('stop_words.txt', HashTableLinear())
    engine = SearchEngine('docs/docs', stopwords)
    while True:
        userInput = input('Enter search query or q to quit: ')
        userInput.lower()
        if userInput == 'q':
            break
        result = engine.search(userInput)
        for idx, (filename, score) in enumerate(result):
            print('File: %s\t Score: %s' % (filename, score))
        print('Search Over\n')

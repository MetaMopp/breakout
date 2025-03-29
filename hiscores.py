import os.path

class HiScores:
    # create a new HiScores table that will be saved to filename
    # if filename already exists, scores will be read from it.
    def __init__(self, filename):
        self._filename = filename
        self._scores = []
        if os.path.exists(self._filename):
            self._read()

    # add an entry to the table. The table will be automatically sorted and saved
    def add(self, score, name):
        self._scores.append([score, name])
        self._sort()
        self._write()

    # returns the number of entries in the table
    def len(self):
        return len(self._scores)

    # returns the entry at a given position, or [0, '-'] if there is no such entry
    def get_entry_at(self, rank):
        if rank < self.len() and rank >= 0:
            return self._scores[rank]
        else:
            return [0, '-']

    # internal methods; no need to call these from outside this class
    def _read(self): # read all scores from file
        with open(self._filename, 'r') as f:
            for line in f:
                fields = line.strip().split('\t')
                self._scores.append([int(fields[0]), fields[1]])
        self._sort()

    def _write(self): # write all scores to file
        with open(self._filename, 'w') as f:
            for entry in self._scores:
                f.write(str(entry[0]) + '\t' + entry[1] + '\n')

    def _sort(self): # sort list
        self._scores.sort(reverse=True)

# Test Code
if __name__ == '__main__':
    hi_scores = HiScores('hiscores.csv')
    hi_scores.add(17, 'seventeen')
    hi_scores.add(13, 'thirteen')
    hi_scores.add(21, 'twentyone')

    print(hi_scores.len())
    for rank in range(4):
        print(rank, ': ', hi_scores.get_entry_at(rank))

    new_scores = HiScores('hiscores.csv')
    print(new_scores.len())
    for rank in range(8):
        print(rank, ': ', new_scores.get_entry_at(rank))

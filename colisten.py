# Build colisten matrix from triplet CSV and save in mtx format
# Usage: python colisten.py <infile> <outfile>

import scipy.sparse, scipy.io
import sys
import util

infile, outfile = sys.argv[1:]

colisten = scipy.sparse.lil_matrix((util.N_SONGS, util.N_SONGS))

for listens in util.songs_by_user(infile):
  for s, _ in listens:
    for t, _ in listens:
      colisten[s-1, t-1] += 1 # Songs are 1-indexed, but scipy uses 0-indexing

scipy.io.mmwrite(file(outfile, 'wb'), colisten)
# Build colisten matrix from triplet CSV and save in mtx format
# Usage: python colisten.py <infile> <outfile>

import scipy.sparse, scipy.io
import sys

N_SONGS = 386213

infile, outfile = sys.argv[1:3]

old_user = 1
listens = []

colisten = scipy.sparse.lil_matrix((N_SONGS, N_SONGS))

for line in open(infile):
  try:
    user, song, _ = [int(x) for x in line.split(',')]
  except ValueError:
    continue
  if old_user != user:
    for s in listens:
      for t in listens:
        colisten[s-1, t-1] += 1 # Songs are 1-indexed, but scipy uses 0-indexing
    listens = []
  listens.append(song)

for s in listens:
  for t in listens:
    colisten[s-1, t-1] += 1

scipy.io.mmwrite(file(outfile, 'wb'), colisten)
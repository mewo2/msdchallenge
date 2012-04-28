# Do prediction based on colistening matrix
# Usage: python predict_colisten.py <mtxfile> <evalfile> <outfile> 

import sys
import scipy.io
import numpy
import util

mtxfile, evalfile, outfile = sys.argv[1:]

colisten = scipy.io.mmread(file(mtxfile)).tocsr()
listens = colisten.diagonal()

with open(outfile, 'w') as out:
  for history in util.songs_by_user(evalfile):
    songs, counts = zip(*history)
    songs = numpy.array(songs)
    
    sim = numpy.ravel(numpy.sum(counts * colisten[songs - 1,:].todense(), 0))
    ranked = numpy.flipud(numpy.lexsort((listens, sim)) + 1)
    
    guess = []
    for s in ranked:
      if s in songs:
        continue
      guess.append(str(s))
      if len(guess) == 500: break
      
    out.write(' '.join(guess) + '\n')
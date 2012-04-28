# Do prediction based on colistening matrix
# Usage: python predict_colisten.py <mtxfile> <evalfile> <outfile> 

import sys
import scipy.io
import numpy
import util

mtxfile, evalfile, outfile = sys.argv[1:]

colisten = scipy.io.mmread(file(mtxfile)).tocsr()
listens = colisten.diagonal()

listenranked = numpy.argsort(-listens)[:500]

with open(outfile, 'w') as out:
  for history in util.songs_by_user(evalfile):
    songs, counts = zip(*history)
    
    sim = numpy.array(counts)[numpy.newaxis, :] * colisten[numpy.array(songs) - 1,:]
        
    # All this nonsense is an optimization to avoid the fact that
    # sorting 300,000 numbers 110,000 times is bad for your health.
    # I only sort the songs where sim > 0
    simidxs = sim.nonzero()[1]
    srt = numpy.lexsort((-listens[simidxs], -sim[0,simidxs]))
    rankidxs = simidxs[srt]
    
    guess = []
    for s in rankidxs:
      if s+1 in songs:
        continue
      guess.append(str(s+1))
      if len(guess) == 500: break
    else:
      for s in listenranked:
        if s+1 in songs or s in rankidxs:
          continue
        guess.append(str(s+1))
        if len(guess) == 500: break
      
    out.write(' '.join(guess) + '\n')

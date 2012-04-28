# Utility functions and constants

N_SONGS = 386213
N_USERS = 110000

def songs_by_user(filename):
  listens = []
  old_user = 1
  for line in open(filename):
    try:
      user, song, count = [int(x) for x in line.split(',')]
    except ValueError:
      continue
    if old_user != user:
      yield listens
      listens = []
      old_user = user
    listens.append((song, count))
  yield listens
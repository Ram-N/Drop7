import numpy as np

chain = {1:7, 2:39, 3:109, 4:224, 5: 391, 6:617, 7:907, 8:1267, 9:1701, 10:2207}

class _Stats(object):
    

    def reset(_outfile):
        _Stats.ball_count = 0
        _Stats.levelup_count = 0
        _Stats.points = 0
        _Stats.nz = []
        _Stats.ptslist, _Stats.explist = [], []
        
        print("", file=open(_outfile, "w"))
        
    def ball_drop():
        _Stats.ball_count += 1
        
    def level_up():
        _Stats.levelup_count += 1
        
    def award_points(chain_level, explosions):
        _Stats.points +=  chain[chain_level] * explosions
        _Stats.ptslist.append(chain[chain_level] * explosions)
        _Stats.explist.append(explosions)

    def update_nz(numnz):
        _Stats.nz.append(numnz)
    

def print_game_over(grid, s):
    print("GAME OVER")
    print(grid)
    print(np.count_nonzero(grid))
    print("DONE")
    print(s.ball_count, s.levelup_count, s.points)
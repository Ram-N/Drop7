import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random 

import cfg


def grid_of_ones(size=cfg._SIZE):
    return np.ones((size,size), dtype=np.int)



def apply_gravity_to_column(column):
    '''
    An entire column is adjusted for 'gravity.' All the zeros float to the top.
    All the other numbers come down as needed.
    '''

    original = column[:] #original
    updated  = column[:] #this can be changed
    flip_flag = 1
    safety_brkr = 0
    flip_occurred = False
    
    while flip_flag:
        a = updated[:]
        safety_brkr += 1
        flip_flag = 0 # off
        for index, (up, down) in enumerate(zip(a[:-1], a[1:])):        
            if up and not down:
                updated[index], updated[index+1] = 0, up
                # print("After ", index, "Column looks like:", column)
                flip_flag = 1 # at least one flip happened, so keep going
                flip_occurred = True
                if safety_brkr >= 100:
                    flip_flag = 0
                    
    return (flip_occurred, original, updated)

from itertools import groupby

def mask(vec):
    return([x > 0 for x in vec])


def get_mask_lengths(_vec):
    '''
    Outputs a tuple of rle lengths, 0's and 1's and their rle's
    '''
    
    m = mask(_vec)
    b = range(len(m))
    ml = []
    for group in groupby(iter(b), lambda x: m[x]): # use m[x] as the grouping key.
        ml.append((group[0], len(list(group[1])))) #group[0] is 1 or 0. and group[1] is its rle

    return ml


def blank_out(_num, vec):
    return [0 if x ==_num else x for x in vec]


def inplace_explosions(vec):
    
    exp_occurred = False
    
    original = [x for x in vec] #manually creating a deepcopy
    updated_vec = [x for x in vec] #manually creating a deepcopy

    ml = get_mask_lengths(updated_vec) # number of contiguous non-zeros
        #print(ml)
    start, end = 0, 0
    for piece in ml:
        _facevalue, _runlen = piece[0], piece[1]
        start = end
        end = start + _runlen
        #print(vec[start:end])
        if _facevalue: #True, nonzero elements exist        
            seg = updated_vec[start:end]
            exploded_seg = blank_out(_runlen, seg)
            if(seg != exploded_seg):
                exp_occurred = True
                updated_vec[start:end] = exploded_seg[:]

    #this is a list of all the elements that remained unchanged. This is the !MASK of changes            
    unchanged = [1 if i==j else 0 for i,j in zip(original, updated_vec)]
                
    # print("Exp occurred", exp_occurred)
    return (exp_occurred, original, unchanged)

def _orig_inplace_explosions(vec):
    """
    In this def, we loop until ALL the explosions are taken care of.
    But the 'right' way to do it seems to be to do one pass.
    Then return the mask. Apply Gravity etc. and come back here.
    """

    potential = True
    exp_occurred = False
    
    original = [x for x in vec] #manually creating a deepcopy
    updated = [x for x in vec] #manually creating a deepcopy
    while potential:
        potential = False
        ml = get_mask_lengths(updated) # number of contiguous non-zeros
        #print(ml)
        start, end = 0, 0
        for piece in ml:
            _len = piece[1]
            start = end
            end = start + _len
            #print(vec[start:end])
            if piece[0]: #True, nonzero elements exist        
                seg = updated[start:end]
                newseg = blank_out(_len, seg)
                if(seg != newseg):
                    potential = True # there could be more explosions
                    exp_occurred = True
                    updated[start:end] = newseg[:]

    unchanged = [1 if i==j else 0 for i,j in zip(original, updated)]
                
    # print("Exp occurred", exp_occurred)
    return (exp_occurred, original, unchanged)



     
def nz(grid):
    return np.count_nonzero(grid)

def is_grid_full(grid):
    nz = np.count_nonzero(grid)
    return nz == (cfg._SIZE * cfg._SIZE)
    
def drop_ball_in_column(grid, ball, col):
    '''
    If valid column, find the first zero in the column and replace the value there.
    If column is full, return illegal flag
    If grid is full game_over
    '''
    game_over = is_grid_full(grid)
    gcol = grid[:, col]
    slot = np.where(gcol==0)[0]
    if not slot.size: #returned []
        need_another_col = True
    else:
        need_another_col = False

    if not game_over and not need_another_col:
        grid[slot[-1], col] = ball # place in the last zero column, from the top
        
    if game_over:
        need_another_col = False
  
        
    return(grid, game_over, need_another_col)



###############################
####### UPDATING GRID #########
###############################

def apply_explosions_to_grid(grid, s, chain_level):

    original = grid.copy() #need this for calculating points
    explosions = 0
    
    # for each row, calculate explosions (but don't execute them)
    # for each col, caluclate explosions (but don't execute them)
    row_mask, col_mask = grid_of_ones(cfg._SIZE), grid_of_ones(cfg._SIZE)
    for i in range(cfg._SIZE):
        _, _, row_mask[i, :] = inplace_explosions(grid[i, :])
        _, _, col_mask[:, i] = inplace_explosions(grid[:, i])
        
        
    # Executing all the explosions at once  
    for i in range(cfg._SIZE):
        grid[i, :] = grid[i, :] * row_mask[i, :]
        grid[:, i] = grid[:, i] * col_mask[:, i]
        
    #print("Came in with", original)
    #print("ROW MASK", row_mask)
    #print("COL MASK", col_mask)    
    #print("After applying Explosions", original, grid)

    #Explosions is the NUMBER of BALLS that EXPLODE at a give grid configuration
    explosions = np.count_nonzero(original!=grid)
    # print("Explosions", explosions)
    # if explosions == 2:
    #    print(original, grid)
    explosions_done = (explosions == 0)
    if chain_level>1:
        print("Chain Level:", chain_level, file=open(cfg._outfile, "a"))
        s.award_points(chain_level, explosions)

    return(grid, explosions_done)


def apply_gravity_to_grid(grid):    
    
    original = grid.copy()
    for i in range(cfg._SIZE):
        _,_,grid[:, i] = apply_gravity_to_column(grid[:, i])
            
            
    updated = grid.copy()
    return(grid, np.array_equal(updated, original))

def update_grid(grid, s):

    gravity_done, explosions_done = 0, 0
    chain_level = 0
    while not (gravity_done and explosions_done):
        chain_level += 1
        grid, explosions_done = apply_explosions_to_grid(grid, s, chain_level)
        grid, gravity_done = apply_gravity_to_grid(grid)
        # print("In update grid", explosions_done, gravity_done)
    return grid
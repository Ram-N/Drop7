
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

from cfg import *


def get_column_to_drop_ball(grid, ball):	

    _MAXCOL = grid.shape[0]    
    #need better logic soon
    return random.randint(0, _MAXCOL-1)
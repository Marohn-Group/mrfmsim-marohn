import math

def convert_grid_pts(distance, grid_step):
    """Convert distance to ext points.
    
    :param int distance: distance in the x direction.
    """
    return math.floor(distance/grid_step[0])

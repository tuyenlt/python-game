import pygame
import math
from typing import Tuple, Optional, List

def delay_frame(num_frame):
    pass

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)



def liang_barsky(rect: Tuple[float, float, float, float], 
                 line_start: Tuple[float, float], 
                 line_end: Tuple[float, float]) -> Optional[List[Tuple[float, float]]]:
    """
    Clipping a line segment to a rectangle using the Liang-Barsky algorithm.
    
    Args:
    - rect: Tuple of rectangle coordinates (x_min, y_min, x_max, y_max)
    - line_start: Start point of the line (x1, y1)
    - line_end: End point of the line (x2, y2)
    
    Returns:
    - A list of intersection points if the line intersects the rectangle or lies within it.
    - None if there are no intersections within the segment.
    """
    x_min, y_min, x_max, y_max = rect
    x1, y1 = line_start
    x2, y2 = line_end

    # Differences between start and end points
    dx = x2 - x1
    dy = y2 - y1

    # Initialize p and q for each side of the rectangle
    p = [-dx, dx, -dy, dy]
    q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]

    u1, u2 = 0.0, 1.0  # Parameters for line segment

    for i in range(4):
        if p[i] == 0:  # Line is parallel to one of the rectangle's sides
            if q[i] < 0:
                return None  # Line is outside and parallel to the rectangle
        else:
            u = q[i] / p[i]
            if p[i] < 0:
                u1 = max(u1, u)  # Moving inwards
            else:
                u2 = min(u2, u)  # Moving outwards

    if u1 > u2:
        return None  # No intersection within the segment

    # Calculate intersection points
    clipped_points = (x1 + u1 * dx, y1 + u1 * dy)
    return clipped_points


class TimerCallback:
    def __init__(self, delay_time, call_back_func):
        self.delay_time = delay_time
        self.time_cnt = delay_time
        self.call_back_func = call_back_func
        self.done = False
        self.finished = True
    
    def count_down(self, amount):
        self.finished = False
        self.time_cnt -= amount
        print(self.time_cnt)
        if self.time_cnt <= 0:
            self.finished = True
            self.call_back_func()
            self.done = True
            self.time_cnt = self.delay_time
            print("call back finished")
    
    def first_finished(self):
        if self.done:
            self.done = False
            return True
        return False        
import pygame
import math
from typing import Tuple, Optional, List

def delay_frame(num_frame):
    pass

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def line_rectangle_collision_point(line, rect):
    # line is defined by two points (x1, y1) and (x2, y2)
    (x1, y1), (x2, y2) = line
    # rect is defined by its top-left corner (rx, ry), width (rw), and height (rh)
    rx, ry, rw, rh = rect
    
    # Define the four corners of the rectangle
    rect_corners = [
        (rx, ry), (rx + rw, ry),      # Top-left to top-right
        (rx + rw, ry + rh), (rx, ry + rh)  # Bottom-right to bottom-left
    ]
    
    # Define rectangle edges as pairs of points
    rect_edges = [
        (rect_corners[0], rect_corners[1]),  # Top edge
        (rect_corners[1], rect_corners[2]),  # Right edge
        (rect_corners[2], rect_corners[3]),  # Bottom edge
        (rect_corners[3], rect_corners[0])   # Left edge
    ]
    
    # Helper function to find the intersection point of two line segments (p1, p2) and (q1, q2)
    def get_intersection_point(p1, p2, q1, q2):
        # Calculate the direction and denominator for the intersection formula
        A1 = p2[1] - p1[1]
        B1 = p1[0] - p2[0]
        C1 = A1 * p1[0] + B1 * p1[1]
        
        A2 = q2[1] - q1[1]
        B2 = q1[0] - q2[0]
        C2 = A2 * q1[0] + B2 * q1[1]
        
        denominator = A1 * B2 - A2 * B1
        
        # If denominator is 0, the lines are parallel (no intersection)
        if denominator == 0:
            return None
        
        # Calculate intersection point
        x = (B2 * C1 - B1 * C2) / denominator
        y = (A1 * C2 - A2 * C1) / denominator
        
        # Check if the intersection point lies on both segments
        if on_segment(p1, p2, (x, y)) and on_segment(q1, q2, (x, y)):
            return (x, y)
        return None

    # Helper function to check if point p lies on segment ab
    def on_segment(a, b, p):
        return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

    # Check intersection between the line and each rectangle edge
    for edge in rect_edges:
        intersection = get_intersection_point((x1, y1), (x2, y2), edge[0], edge[1])
        if intersection:
            return intersection  # Return the first collision point found

    return None  # No collision point found




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
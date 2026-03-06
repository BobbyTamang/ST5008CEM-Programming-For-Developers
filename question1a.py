from math import gcd
from collections import defaultdict

def max_points_on_line(points):
    """
    Calculates the maximum number of points that lie on the same straight line.
    Uses GCD to represent slopes as normalized fractions to avoid floating-point errors.
    """
    n = len(points)
    if n <= 2: return n
    
    max_count = 0
    for i in range(n):
        slopes = defaultdict(int)
        duplicate_points = 1
        current_max = 0
        
        for j in range(i + 1, n):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            
            if dx == 0 and dy == 0:
                duplicate_points += 1
                continue
                
            # Normalize the slope using Greatest Common Divisor
            common = gcd(dx, dy)
            slope = (dx // common, dy // common)
            
            slopes[slope] += 1
            current_max = max(current_max, slopes[slope])
            
        max_count = max(max_count, current_max + duplicate_points)
        
    return max_count

# Example Test Case [cite: 19]
print(f"Max Points: {max_points_on_line([[1,1],[2,2],[3,3]])}") # Output: 3
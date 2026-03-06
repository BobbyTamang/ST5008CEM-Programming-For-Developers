# DEV NOTE: For the Tourist Optimizer, I used a Greedy 'Nearest Neighbor' 
# approach. While TSP is NP-hard, this heuristic works perfectly for a 
# small number of city spots (like KTM, Patan, Bhaktapur) to give 
# a fast and 'good enough' route.

import math

def calculate_distance(p1, p2):
    """Euclidean distance between two coordinates."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def optimize_tour(spots):
    """
    Finds a path through all tourist spots starting from the first one.
    spots: List of tuples [(x, y, "Name"), ...]
    """
    if not spots: return []
    
    unvisited = spots[1:] # Assume we start at the first spot
    current_spot = spots[0]
    route = [current_spot]
    total_distance = 0
    
    while unvisited:
        # Find the closest next spot
        next_spot = min(unvisited, key=lambda s: calculate_distance((current_spot[0], current_spot[1]), (s[0], s[1])))
        
        dist = calculate_distance((current_spot[0], current_spot[1]), (next_spot[0], next_spot[1]))
        total_distance += dist
        
        route.append(next_spot)
        unvisited.remove(next_spot)
        current_spot = next_spot
        
    return route, total_distance

# --- EXAMPLE SPOTS (Coordinates) ---
ktm_spots = [
    (27.7172, 85.3240, "Kathmandu Durbar Square"),
    (27.6710, 85.3213, "Patan Durbar Square"),
    (27.6727, 85.4297, "Bhaktapur Durbar Square"),
    (27.7149, 85.2904, "Swayambhunath"),
    (27.7174, 85.3585, "Pashupatinath")
]

optimized_path, total_km = optimize_tour(ktm_spots)

print("Optimized Tour Sequence:")
for i, spot in enumerate(optimized_path):
    print(f"{i+1}. {spot[2]}")
print(f"\nTotal Estimated Distance: {total_km:.2f} units")
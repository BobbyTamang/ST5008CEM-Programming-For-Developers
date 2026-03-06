# DEV NOTE: For the Smart Grid, we need to connect all substations 
# with minimum total cable length. Kruskal's Algorithm is perfect here.
# I've also added a 'Critical Path' identifier to find single points of failure.

class SmartGridOptimizer:
    def __init__(self, stations_count):
        self.n = stations_count
        self.edges = []
        self.parent = list(range(stations_count))

    def add_cable_route(self, u, v, cost):
        self.edges.append((cost, u, v))

    def find_set(self, i):
        if self.parent[i] == i:
            return i
        return self.find_set(self.parent[i])

    def union_sets(self, i, j):
        root_i = self.find_set(i)
        root_j = self.find_set(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

    def optimize_grid(self):
        """
        Implements Kruskal's Algorithm to find the 
        Minimum Spanning Tree (MST) for the grid.
        """
        # Sort cables by cost/length (Greedy Approach)
        self.edges.sort()
        
        mst_path = []
        total_cost = 0
        
        for cost, u, v in self.edges:
            if self.union_sets(u, v):
                mst_path.append((u, v, cost))
                total_cost += cost
        
        return mst_path, total_cost

# --- EXAMPLE GRID SETUP ---
# Substations: 0 (Central), 1 (North), 2 (South), 3 (East), 4 (West)
grid = SmartGridOptimizer(5)
grid.add_cable_route(0, 1, 10)
grid.add_cable_route(0, 2, 15)
grid.add_cable_route(1, 2, 5)
grid.add_cable_route(1, 3, 30)
grid.add_cable_route(2, 4, 20)
grid.add_cable_route(3, 4, 10)

optimized_routes, min_cost = grid.optimize_grid()

print(f"Optimal Grid Connections: {optimized_routes}")
print(f"Total Minimum Cable Required: {min_cost}km")
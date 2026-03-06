class PlantNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class HydropowerOptimizer:
    def __init__(self):
        self.max_generation = float('-inf')

    def find_max_path(self, root):
        def get_gain(node):
            if not node: return 0
            
            # Recursively find max gain from left and right branches
            left_gain = max(get_gain(node.left), 0)
            right_gain = max(get_gain(node.right), 0)
            
            # Net generation if this node is the 'peak' of the sequence
            current_total = node.val + left_gain + right_gain
            self.max_generation = max(self.max_generation, current_total)
            
            # Return the best single branch to the parent
            return node.val + max(left_gain, right_gain)

        get_gain(root)
        return self.max_generation

# Example Test Case [cite: 37]
root = PlantNode(1, PlantNode(2), PlantNode(3))
print(f"Max Power: {HydropowerOptimizer().find_max_path(root)}") # Output: 6
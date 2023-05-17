class node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.heuristicCost = 0
        self.depth = 0
        self.leftChild = None
        self.rightChild = None
        self.upChild = None
        self.downChild = None
        self.expanded = False
#The node class in this program represents a state in the 8-puzzle problem. It stores the 
# current puzzle configuration, the depth of the node in the search tree, the heuristic 
# cost associated with the node, and four child nodes. The four child nodes correspond to the 
# possible moves of the empty tile (0) in the puzzle. Additionally, the node has an expanded 
# boolean flag that indicates whether it has been expanded during the search process.
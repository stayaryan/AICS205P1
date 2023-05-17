from node import node
import copy
#The function expansionOfStates(nodeDefinition, s) expands the given node by generating its child 
# nodes based on the possible moves of the empty tile (0) in the puzzle configuration.
def expansionOfStates(nodeDefinition, s):
    row = 0
    col = 0
#First, it determines the position of the empty tile in the puzzle. Then, it checks four possible moves:
#  left, right, up, and down.
    for i in range(len(nodeDefinition.puzzle)):
        for j in range(len(nodeDefinition.puzzle)):
            if nodeDefinition.puzzle[i][j] == 0:
                row = i
                col = j
#If the empty tile is not in the first column, it creates a new child node by swapping the empty tile 
# with the tile to its left (column-wise). The new puzzle configuration is stored in the left variable,
#  and if this configuration has not been encountered before (not present in set s), a new child node 
# is created with the left configuration.
    if col > 0:
        left = copy.deepcopy(nodeDefinition.puzzle)
        temp = left[row][col]
        left[row][col] = left[row][col - 1]
        left[row][col - 1] = temp

        if left not in s:
            nodeDefinition.leftChild = node(left)
#If the empty tile is not in the last column, it creates a new child node by swapping the empty tile 
# with the tile to its right (column-wise). The new puzzle configuration is stored in the right variable,
#  and if it is not in set s, a new child node is created
    if col < len(nodeDefinition.puzzle)-1:
        right = copy.deepcopy(nodeDefinition.puzzle)
        temp = right[row][col]
        right[row][col] = right[row][col+1]
        right[row][col+1] = temp

        if right not in s:
            nodeDefinition.rightChild = node(right)
#If the empty tile is not in the first row, it creates a new child node by swapping the empty tile with 
# the tile above it (row-wise). The new puzzle configuration is stored in the up variable, and if it is 
# not in set s, a new child node is created.
    if row > 0:
        up = copy.deepcopy(nodeDefinition.puzzle)
        temp = up[row][col]
        up[row][col] = up[row - 1][col]
        up[row - 1][col] = temp

        if up not in s:
            nodeDefinition.downChild = node(up)
#If the empty tile is not in the last row, it creates a new child node by swapping the empty tile with 
# the tile below it (row-wise). The new puzzle configuration is stored in the down variable, and if it 
# is not in set s, a new child node is created.
    if row < len(nodeDefinition.puzzle) - 1:
        down = copy.deepcopy(nodeDefinition.puzzle)
        temp = down[row][col]
        down[row][col] = down[row + 1][col]
        down[row + 1][col] = temp

        if down not in s:
            nodeDefinition.upChild = node(down)
    #Finally, the function returns the updated nodeDefinition with the generated child nodes.
    return nodeDefinition

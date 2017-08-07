# -*- coding: utf-8 -*-

class Node(object):
    """ A Node in a kd-tree
    A tree is represented by its root node, and every node represents
    its subtree
    """

    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


    @property
    def is_leaf(self):
        """
        Returns True if a Node has no subnodes
        """
        return (self.left is None and self.right is None)


    def set_child(self, index, child):
        """ Sets one of the node's children
        index 0 refers to the left, 1 to the right child
        """
        if index == 0:
            self.left = child
        else:
            self.right = child


class KDTree(object):
    def __init__(self, data=[], k=2):
        self.k = k
        self.root = self.init_tree(data, 0)

    def init_tree(self, data=[], axis=0) -> Node:
        if data is None or len(data) == 0:
            return None

        if len(data) == 1:
            return Node(data[0], None, None)

        sort_data = sorted(data, key = lambda x: x[axis])
        data_length = len(sort_data)
        split_index = int(data_length / 2)

        left_data = sort_data[:split_index]
        median_data = sort_data[split_index : split_index + 1]
        right_data = sort_data[split_index + 1:]

        next_axis = (axis + 1) % self.k
        left = self.init_tree(left_data, next_axis)
        right = self.init_tree(right_data, next_axis)
        parent = Node(median_data[0], left, right)

        return parent

    def preorder(self):
        """
        iterator for nodes: root, left, right
        """
        stack = []
        if (self.root is not None):
            stack.append(self.root)

        while (len(stack) > 0):
            current = stack.pop()
            print(current.data)

            left = current.left
            right = current.right

            if right is not None:
                stack.append(right)
            if left is not None:
                stack.append(left)

    def search_nn(self, node_data: []) -> Node:
        return self.root

if __name__ == '__main__':
    data = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7]]
    tree = KDTree(data, 2)
    tree.preorder()

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


class KDTree(object):
    def __init__(self, data_list=[], k=2):
        self.k = k
        self.root = self.init_tree(data_list, 0)

    def init_tree(self, data_list=[], axis=0) -> Node:
        if data_list is None or len(data_list) == 0:
            return None

        if len(data_list) == 1:
            return Node(data_list[0], None, None)

        sort_data = sorted(data_list, key = lambda x: x[axis])
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


    def path_nn(self, root: Node, point: []) -> []:
        """
        path from root to leaf for given data
        :param root: tree node
        :param point: search data
        :return:
        """
        node_list = []
        current = root
        depth = 0

        while current is not None :
            axis = depth % self.k
            next = current.left if point[axis] < current.data[axis] else current.right
            depth += 1
            node_list.append(current)
            current = next

        return node_list


    def search_nn(self, root: Node, point: []) -> Node:
        nearest = root
        prev = None

        # path from root to leaf
        node_list = self.path_nn(root, point)
        while len(node_list) > 0:
            current = node_list.pop()

            if (self.distance(current.data, point) <= self.distance(nearest.data, point)):
                nearest = current
                # the other child
                other_child = current.right if current.left == prev else current.left
                if other_child is not None:
                    child_nearest = self.search_nn(other_child, point)
                    if (self.distance(child_nearest.data, point) < self.distance(nearest.data, point)):
                        nearest = child_nearest

            prev = current

        return nearest


    def distance(self, point1: [], point2: []):
        length = len(point1)
        dist = 0
        for i in range(0, length):
            dist += (point1[i] - point2[i]) ** 2
        dist = dist ** 0.5
        return dist


if __name__ == '__main__':
    data = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7]]
    tree = KDTree(data, 2)
    nearest = tree.search_nn(tree.root, [5, 5.5])
    print(nearest.data)
# Name: Tyler Renn
# OSU Email: rennt@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: A04
# Due Date: 05/22/2023 @ 11:59 PM
# Description: Add methods to the current BST class to add()
#               remove() nodes.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree
        """

        node = BSTNode(value)
        n = self._root
        p = None

        # Loop used to Traverse down BST
        while n is not None:
            p = n

            # Checks if value being inserted needs to be added
            # as the left or right child
            if value < n.value:
                n = n.left
            else:
                n = n.right

        # If BST was initially empty
        if p is None:
            p = node
            self._root = p

        elif value < p.value:
            p.left = node

        else:
            p.right = node

    def remove(self, value: object) -> bool:
        """
        This method removes a value from the tree. The method returns
        True if the value is removed. Otherwise, it returns False
        """

        p = None
        n = self._root

        # Find the node to remove and its parent
        while n:
            if value == n.value:
                break
            p = n
            if value < n.value:
                n = n.left
            else:
                n = n.right
        else:
            # Value not found in the tree
            return False

        if n.left is None and n.right is None:
            # Case 1: Node to remove has no children
            if p is None:
                self._root = None
            elif p.left is n:
                p.left = None
            else:
                p.right = None
        elif n.left is None:
            # Case 2: Node to remove has only right child
            if p is None:
                self._root = n.right
            elif p.left is n:
                p.left = n.right
            else:
                p.right = n.right
        elif n.right is None:
            # Case 3: Node to remove has only left child
            if p is None:
                self._root = n.left
            elif p.left is n:
                p.left = n.left
            else:
                p.right = n.left
        else:
            # Case 4: Node to remove has both left and right children
            successor_p = n
            successor = n.right

            while successor.left:
                successor_p = successor
                successor = successor.left

            n.value = successor.value

            if successor_p.left is successor:
                successor_p.left = successor.right
            else:
                successor_p.right = successor.right

        return True

    def contains(self, value: object) -> bool:
        """
        This method returns True if the value is in the tree.
        Otherwise, it returns False
        """
        n = self._root

        if n is None:
            return False

        # This code initializes a stack object and pushes
        # the root node (n) onto the stack to start the traversal.
        stack = Stack()
        stack.push(n)

        # This code enters a while loop that
        # continues until the stack is empty,
        # indicating that all nodes have been processed.
        while not stack.is_empty():
            n = stack.pop()

            if n.value == value:
                return True

            if n.left:
                stack.push(n.left)
            if n.right:
                stack.push(n.right)

        return False

    def inorder_traversal(self) -> Queue:
        """
        This method will perform an
        inorder traversal of the tree and return a
        Queue object that contains the values of the visited nodes, in the order they were visited.
        If the tree is empty, the method returns an empty Queue
        """
        traversal = Queue()
        n = self._root

        if n is None:
            return traversal

        stack = Stack()

        # Loop that continues until the current node is node
        # and until the stack is empty
        while n or not stack.is_empty():

            # Traverses the left most side by pushing each node
            # unto the stack. Once it reaches the left most node,
            # it pops a node from the stack,
            # adds its value to the traversal queue,
            # and moves to its right child.
            while n:
                stack.push(n)
                n = n.left

            n = stack.pop()
            traversal.enqueue(n.value)

            n = n.right

        return traversal

    def find_min(self) -> object:
        """
        This method returns the lowest value in the tree. If the tree is empty, the method should
        return None
        """
        n = self._root

        if n is None:
            return

        p = self._root

        while p.left:
            p = p.left

        return p.value

    def find_max(self) -> object:
        """
        This method returns the highest value in the tree
        """
        n = self._root

        if n is None:
            return

        p = self._root

        while p.right:
            p = p.right

        return p.value

    def is_empty(self) -> bool:
        """
        This method returns True if the tree is empty.
        """
        n = self._root

        if n is None:
            return True

        return False

    def make_empty(self) -> None:
        """
        Empties the BST
        """

        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

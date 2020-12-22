"""
Project 3 (Fall 2020) - Red/Black Trees
Name: Solution
"""

from __future__ import annotations
from typing import TypeVar, Generic, Callable, Generator
from Project3.RBnode import RBnode as Node
from copy import deepcopy
import queue

T = TypeVar('T')


class RBtree:
    """
    A Red/Black Tree class
    :root: Root Node of the tree
    :size: Number of Nodes
    """

    __slots__ = ['root', 'size']

    def __init__(self, root: Node = None):
        """ Initializer for an RBtree """
        # this allows us to initialize by copying an existing tree
        self.root = deepcopy(root)
        if self.root:
            self.root.parent = None
        self.size = 0 if not self.root else self.root.subtree_size()

    def __eq__(self, other: RBtree) -> bool:
        """ Equality Comparator for RBtrees """
        comp = lambda n1, n2: n1 == n2 and ((comp(n1.left, n2.left) and comp(n1.right, n2.right)) if (n1 and n2) else True)
        return comp(self.root, other.root) and self.size == other.size

    def __str__(self) -> str:
        """ represents Red/Black tree as string """

        if not self.root:
            return 'Empty RB Tree'

        root, bfs_queue, height = self.root, queue.SimpleQueue(), self.root.subtree_height()
        track = {i: [] for i in range(height+1)}
        bfs_queue.put((root, 0, root.parent))

        while bfs_queue:
            n = bfs_queue.get()
            if n[1] > height:
                break
            track[n[1]].append(n)
            if n[0] is None:
                bfs_queue.put((None, n[1]+1, None))
                bfs_queue.put((None, n[1]+1, None))
                continue
            bfs_queue.put((None, n[1]+1, None) if not n[0].left else (n[0].left, n[1]+1, n[0]))
            bfs_queue.put((None, n[1]+1, None) if not n[0].right else (n[0].right, n[1]+1, n[0]))

        spaces = 12*(2**height)
        ans = '\n' + '\t\tVisual Level Order Traversal of RBtree'.center(spaces) + '\n\n'
        for i in range(height):
            ans += f"Level {i+1}: "
            for n in track[i]:
                space = int(round(spaces / (2**i)))
                if not n[0]:
                    ans += ' ' * space
                    continue
                ans += "{} ({})".format(n[0], n[2].value if n[2] else None).center(space, " ")
            ans += '\n'
        return ans

    def __repr__(self) -> str:
        return self.__str__()

################################################################
################### Complete Functions Below ###################
################################################################

######################## Static Methods ########################
# These methods are static as they operate only on nodes, without explicitly referencing an RBtree instance

    @staticmethod
    def set_child(parent: Node, child: Node, is_left: bool) -> None:
        """
        Sets the child parameter of parent to a child node.
        The parent parameter of the new child node should be updated as required.
        :param parent: parent of the child
        :param child: the child node
        :param is_left: determines which child will be set
        :return: None
        """
        if is_left is True:
            parent.left = child
        else:
            parent.right = child

    @staticmethod
    def replace_child(parent: Node, current_child: Node, new_child: Node) -> None:
        """
        Replaces parent's current child node with a new child node.
        :param parent: parent node
        :param current_child: current child node that will be replaced
        :param new_child: replacement node
        :return: None
        """
        if parent.left == current_child:
            RBtree.set_child(parent, new_child, True)
        elif parent.right == current_child:
            RBtree.set_child(parent, new_child, False)

    @staticmethod
    def get_sibling(node: Node) -> Node:
        """
        Gets the sibling of a given node.
        :param node: child node that needs to find its sibling
        :return: the other child of that node's parent, or None if no parent exists
        """
        par = node.parent
        if par is None:
            return None
        if par.left is node:
            return par.right
        return par.left

    @staticmethod
    def get_grandparent(node: Node) -> Node:
        """
        Get the grandparent of given node.
        :param node: node to find the grandparent of
        :return: grandparent node
        """
        par = node.parent
        if par is None:
            return None
        return par.parent

    @staticmethod
    def get_uncle(node: Node) -> Node:
        """
        Get the uncle of given node.
        :param node: node to find the uncle of
        :return: uncle node
        """
        par = node.parent
        if par is None:
            return None
        grand = par.parent
        if grand is None:
            return None
        if par is grand.left:
            return grand.right
        return grand.left

 ######################## Misc Utilities ##########################

    def min(self, node: Node) -> Node:
        """
        Finds the minimum value stored in the subtree rooted at node.
        :param node: root node
        :return: node with minimum value
        """
        if node is None:
            return None

        while node.left is not None:
            node = node.left
        return node

    def max(self, node: Node) -> Node:
        """
        Finds the maximum value stored in the subtree rooted at node.
        :param node: root node
        :return: node with maximum value
        """
        if node is None:
            return None

        while node.right is not None:
            node = node.right
        return node

    def search(self, node: Node, val: Generic[T]) -> Node:
        """
        Searches the subtree rooted at node for a node containing value val.
        :param node: root node
        :param val: node value
        :return: Node
        """
        if node is None:
            return None
        if node.value == val:
            return node
        elif val < node.value and node.left is not None:
            return self.search(node.left, val)
        elif val > node.value and node.right is not None:
            return self.search(node.right, val)
        return node

 ######################## Tree Traversals #########################

    def inorder(self, node: Node) -> Generator[Node, None, None]:
        """
        Inorder traversal of the subtree.
        :param: root node
        :return: a generator object
        """
        if self.root is None:
            return
        if node.left is not None:
            for other in self.inorder(node.left):
                yield other
        yield node
        if node.right is not None:
            for other in self.inorder(node.right):
                yield other

    def preorder(self, node: Node) -> Generator[Node, None, None]:
        """
        Preorder traversal of the subtree.
        :param node: root node
        :return: A generator object
        """
        if self.root is None:
            return
        yield node
        if node.left is not None:
            for other in self.preorder(node.left):
                yield other
        if node.right is not None:
            for other in self.preorder(node.right):
                yield other

    def postorder(self, node: Node) -> Generator[Node, None, None]:
        """
        Postorder traversal of the subtree.
        :param node: root node
        :return: a generator object
        """
        if self.root is None:
            return
        if node.left is not None:
            for other in self.postorder(node.left):
                yield other
        if node.right is not None:
            for other in self.postorder(node.right):
                yield other
        yield node

    def bfs(self, node: Node) -> Generator[Node, None, None]:
        """
        Breadth first traversal of the subtree.
        :param node: root node
        :return: a generator object (yield)
        """
        if node is None:
            node = self.root

        to_visit = [node]
        while to_visit:
            cur = to_visit.pop(0)
            yield cur
            if cur.left:
                to_visit.append(cur.left)
            if cur.right:
                to_visit.append(cur.right)

 ################### Rebalancing Utilities ######################

    def left_rotate(self, node: Node) -> None:
        """
        Performs a left tree rotation on the subtree rooted at node.
        :param node: node that will be performed on
        :return: None
        """
        if node is None:
            return None

        y = node.right
        node.right = y.left
        if y.left is not None:
            y.left.parent = node

        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def right_rotate(self, node: Node) -> None:
        """
        Performs a right tree rotation on the subtree rooted at node.
        :param node: node that will be performed on
        :return: None
        """
        if node is None:
            return None

        y = node.left
        node.left = y.right
        if y.right is not None:
            y.right.parent = node

        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

    def insertion_repair(self, node: Node) -> None:
        """
        This method is not tested explicitly, but should be called
        after insertion on the node which was inserted, and should
        re-balance the tree by ensuring adherence to Red/Black properties.
        :param node: inserted node
        :return: None
        """
        if node.parent is None:
            node.is_red = False
            return None
        if node.parent.is_red is False:
            return None
        parent = node.parent
        grandparent = RBtree.get_grandparent(node)
        uncle = RBtree.get_uncle(node)

        if uncle is not None and uncle.is_red is True:
            parent.is_red = False
            uncle.is_red = False
            grandparent.is_red = True
            self.insertion_repair(grandparent)
            return None

        if node is parent.right and parent is grandparent.left:
            self.left_rotate(parent)
            node = parent
            parent = node.parent
        elif node is parent.left and parent is grandparent.right:
            self.right_rotate(parent)
            node = parent
            parent = node.parent
        parent.is_red = False
        grandparent.is_red = True

        if node is parent.left:
            self.right_rotate(grandparent)
        else:
            self.left_rotate(grandparent)

    def prepare_removal(self, node: Node) -> None:
        """
        This method is not tested explicitly, but should be called prior to removal,
        on a node that is to be removed. It should ensure balance is maintained after the removal.
        :param node: node that is to be removed
        :return: None
        """
        def tree_not_none_and_red(root):
            if root is None:
                return False
            if root.is_red is True:
                return True
            return False

        def tree_null_or_black(root):
            if root is None:
                return True
            if root.is_red is False:
                return True
            return False

        def both_children_black(root):
            if root.left is not None and root.left.is_red is True:
                return False
            if root.right is not None and root.right.is_red is True:
                return False
            return True

        # case 1
        if node.is_red or node.parent is None:
            return
        sibling = self.get_sibling(node)
        # case 2
        if sibling.is_red:
            node.parent.is_red = True
            sibling.is_red = False
            if node is node.parent.left:
                self.left_rotate(node.parent)
            else:
                self.right_rotate(node.parent)
            sibling = self.get_sibling(node)
        # case 3
        if (node.parent.is_red is False) and both_children_black(sibling):
            sibling.is_red = True
            self.prepare_removal(node.parent)
            return
        # case 4
        if node.parent.is_red and both_children_black(sibling):
            node.parent.is_red = False
            sibling.is_red = True
            return
        # case 5
        if tree_not_none_and_red(sibling.left) and tree_null_or_black(sibling.right) and node is node.parent.left:
            sibling.is_red = True
            sibling.left.is_red = False
            self.right_rotate(sibling)
            sibling = self.get_sibling(node)
        # case 6
        if tree_null_or_black(sibling.left) and tree_not_none_and_red(sibling.right) and node is node.parent.right:
            sibling.is_red = True
            sibling.right.is_red = False
            self.left_rotate(sibling)
            sibling = self.get_sibling(node)

        sibling.is_red = node.parent.is_red
        node.parent.is_red = False
        if node is node.parent.left:
            sibling.right.is_red = False
            self.left_rotate(node.parent)
        else:
            sibling.left.is_red = False
            self.right_rotate(node.parent)

##################### Insertion and Removal #########################

    def insert(self, node: Node, val: Generic[T]) -> None:
        """
        Inserts an RBnode object to the subtree rooted at node with value val.
        :param node: root node
        :param val: insert node with given value
        :return: None
        """
        if self.root is None:
            self.root = Node(val)
            self.root.is_red = False
            self.size += 1
            return None
        else:
            if val == node.value:
                return None
            elif val < node.value:
                if node.left is None:
                    node.left = Node(val)
                    node.left.parent = node
                    self.size += 1
                    self.insertion_repair(node.left)
                else:
                    self.insert(node.left, val)
            else:
                if node.right is None:
                    node.right = Node(val)
                    node.right.parent = node
                    self.size += 1
                    self.insertion_repair(node.right)
                else:
                    self.insert(node.right, val)

    def remove(self, node: Node, val: Generic[T]) -> None:
        """
        Removes node with value val from the subtree rooted at node.
        If no such node exists, do nothing.
        :param node: root node
        :param val: remove node with given value
        :return: None
        """
        if node is not None:
            self.RBtree_remove(node, val)

    def RBtree_remove(self, node, val):
        """
        Red and Black tree removal of node rooted at given node.
        :param node: root node
        :param val: value of node
        :return: None
        """
        found = self.search(node, val)
        if found is None:
            return

        if node.left is not None and node.right is None:
            pred = node.left
            key = pred.value
            self.RBtree_remove(pred, key)
            node.value = key
            return
        if found.right is not None and found.left is not None:
            pred = self.get_predecessor(found)
            key = pred.value
            self.remove(node, pred.value)
            found.value = key
            return
        if found.is_red is False:
            self.prepare_removal(found)
        self.bst_remove(node, found.value)

    def bst_remove(self, node, val):
        """
        Binary search tree removal of node rooted at given node.
        :param node: root node
        :param val: node value
        :return: None
        """
        found = self.search(node, val)
        if found is None or found.value != val:
            return
        if found.right is None and found.left is None:
            par = found.parent
            if par is None:
                self.root = None
            elif par.right is not None and par.right.value == val:
                par.right = None
            else:
                par.left = None
            self.size -= 1
            return
        if found.right is None or found.left is None:
            par = found.parent
            if found.right is not None:
                child = found.right
            else:
                child = found.left
            if par is None:
                self.root = child
                self.root.is_red = False
            elif par.right is not None and par.right.value == val:
                par.right = child
            else:
                par.left = child
            child.parent = par
            self.size -= 1
            return
        min_right = self.min(found.right)
        self.bst_remove(min_right.value)
        found.value = min_right.value

    def get_predecessor(self, node):
        """
        Gets the predecessor of node
        :param node: node
        :return: node
        """
        node = node.left
        while node.right is not None:
            node = node.right
        return node






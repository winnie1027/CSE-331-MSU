from typing import List, Tuple, Any


class Node:
    """
    Node definition should not be changed in any way
    """
    __slots__ = ['key', 'value']

    def __init__(self, k: Any, v: Any):
        """
        Initializes node
        :param k: key to be stored in the node
        :param v: value to be stored in the node
        """
        self.key = k
        self.value = v

    def __lt__(self, other):
        """
        Less than comparator
        :param other: second node to be compared to
        :return: True if the node is less than other, False if otherwise
        """
        return self.key < other.key or (self.key == other.key and self.value < other.value)

    def __gt__(self, other):
        """
        Greater than comparator
        :param other: second node to be compared to
        :return: True if the node is greater than other, False if otherwise
        """
        return self.key > other.key or (self.key == other.key and self.value > other.value)

    def __eq__(self, other):
        """
        Equality comparator
        :param other: second node to be compared to
        :return: True if the nodes are equal, False if otherwise
        """
        return self.key == other.key and self.value == other.value

    def __str__(self):
        """
        Converts node to a string
        :return: string representation of node
        """
        return '({0}, {1})'.format(self.key, self.value)

    __repr__ = __str__


class PriorityQueue:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = []

    def __str__(self) -> str:
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data)

    __repr__ = __str__

    def to_tree_format_string(self) -> str:
        """
        Prints heap in Breadth First Ordering Format
        :return: String to print
        """
        string = ""
        # level spacing - init
        nodes_on_level = 0
        level_limit = 1
        spaces = 10 * int(1 + len(self))

        for i in range(len(self)):
            space = spaces // level_limit
            # determine spacing

            # add node to str and add spacing
            string += str(self.data[i]).center(space, ' ')

            # check if moving to next level
            nodes_on_level += 1
            if nodes_on_level == level_limit:
                string += '\n'
                level_limit *= 2
                nodes_on_level = 0
            i += 1

        return string

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def __len__(self) -> int:
        """
        Length of queue.
        """
        return len(self.data)

    def empty(self) -> bool:
        """
        Checking if queue is empty.
        """
        return len(self) == 0

    def top(self) -> Node:
        """
        Returns top node of queue.
        """
        if self.empty():
            return None
        return self.data[0]

    def left(self, index: int) -> int:
        """
        Gets left index of node at given index.
        """
        return 2 * index + 1

    def right(self, index: int) -> int:
        """
        Gets right index of node at given index.
        """
        return 2 * index + 2

    def has_left(self, index: int) -> bool:
        """
        Checks if node at given index has a left node.
        :param index: index of node.
        :return: bool
        """
        return self.left(index) < len(self.data)

    def has_right(self, index: int) -> bool:
        """
        Checks if node at given index has a right node.
        :param index: index of node.
        :return: bool
        """
        return self.right(index) < len(self.data)

    def get_left_child_index(self, index: int) -> int:
        """
        Given an index of a node, return the index of the left child.
        In the event that the index has no left child, return None.
        :param index: index of a node.
        :return: int
        """
        if self.has_left(index):
            return 2 * index + 1
        return None

    def get_right_child_index(self, index: int) -> int:
        """
        Given an index of a node, return the index of the right child.
        In the event that the index has no left child, return None.
        :param index: index of a node.
        :return: int
        """
        if self.has_right(index):
            return 2 * index + 2
        return None

    def get_parent_index(self, index: int) -> int:
        """
        Given an index of a node, return the index of its parent.
        In the event that the index is the top of the PriorityQueue, return None.
        :return: int
        """
        if index == 0:
            return None
        return (index - 1) // 2

    def swap(self, i, j) -> None:
        """
        Swaps two elements' placements.
        """
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def push(self, key: Any, val: Any) -> None:
        """
        Use the key and value parameters to add a Node to the heap.
        :return: None
        """
        self.data.append(Node(key, val))
        self.percolate_up(len(self.data)-1)

    def pop(self) -> Node:
        """
        Removes the smallest element from the priority queue.
        :return: popped node
        """
        if self.empty():
            return None
        self.swap(0, len(self.data) - 1)  # put minimum item at the end
        item = self.data.pop()  # and remove it from the list;
        if len(self.data) != 1 and not self.empty():
            self.percolate_down(0)  # then fix new root
        return item

    def get_min_child_index(self, index: int) -> int:
        """
        Given an index of a node, return the index of the smaller child.
        In the event that the index is a leaf, return None.
        :param index: original index.
        :return: index of minimum child.
        """
        left = self.get_left_child_index(index)
        right = self.get_right_child_index(index)
        if self.has_left(index) or self.has_right(index):
            if self.has_left(index) and not self.has_right(index):
                return left
            if self.has_right(index) and not self.has_left(index):
                return right
            if self.has_right(index) and self.has_left(index):
                left_val = self.data[left]
                right_val = self.data[right]
                if left_val < right_val:
                    return left
                if right_val < left_val:
                    return right
        return None

    def percolate_up(self, index: int) -> None:
        """
        Given the index of a node, move the node up to its valid spot in the heap.
        :return: None
        """
        parent = self.get_parent_index(index)
        if index > 0 and self.data[index] < self.data[parent]:
            self.swap(index, parent)
            self.percolate_up(parent)

    def percolate_down(self, index: int) -> None:
        """
        Given the index of a node, move the node down to its valid spot in the heap.
        :return: None
        """
        if self.has_left(index):
            left = self.get_left_child_index(index)
            small_child = left
            if self.has_right(index):
                right = self.get_right_child_index(index)
                if self.data[right] < self.data[left]:
                    small_child = right
            if self.data[small_child] < self.data[index]:
                self.swap(index, small_child)
                self.percolate_down(small_child)


class MaxHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = PriorityQueue()

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data.data)

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self.data)

    def print_tree_format(self):
        """
        Prints heap in bfs format
        """
        self.data.tree_format()

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def empty(self) -> bool:
        """
        Checks if heap is empty.
        """
        return len(self) == 0

    def top(self) -> int:
        """
        Returns top element of heap.
        """
        if self.empty():
            return None
        node = self.data.top()
        value = node.value
        return -value

    def push(self, key: int) -> None:
        """
        Push element onto heap.
        :param key: int
        """
        self.data.push(-key, -key)

    def pop(self) -> int:
        """
        Removes largest element and returns it.
        """
        if self.empty():
            return None
        item = self.data.pop()
        return -item.key


def heap_sort(array) -> list:
    """
    Sorts an array in place by using a Max Heap.
    :param array: an array of integers.
    :return: the same list but sorted.
    """
    heap = MaxHeap()
    for value in array:
        heap.push(-value)
    for i in range(len(heap)):
        array[i] = -heap.pop()
    return array


def find_ranking(rank, results: List[Tuple[int, str]]) -> str:
    """
    Given “results”, a list of tuples – with each tuple containing the amount of
    losses that team suffered and the team name - find the team that finished in
    the position “rank”.
    :param rank: integer.
    :param results: tuples containing a number and team name.
    :return: team name at the appropriate ranking.
    """
    if rank > len(results):
        return None
    pq = PriorityQueue()
    for item in results:
        pq.push(item[0], item[1])
    counter = 0
    team = ""
    for i in range(len(pq)):
        counter += 1
        team = pq.pop()
        if counter == rank:
            break
    return team.value


"""
Winnie Yang
Project 4 - Tries
CSE 331 Fall 2020
Professor Sebnem Onsay
"""

from __future__ import annotations
from typing import Tuple, Dict, List


class TrieNode:
    """
    Implementation of a trie node.
    """

    # DO NOT MODIFY

    __slots__ = "children", "is_end"

    def __init__(self, arr_size: int = 26) -> None:
        """
        Constructs a TrieNode with arr_size slots for child nodes.
        :param arr_size: Number of slots to allocate for child nodes.
        :return: None
        """
        self.children = [None] * arr_size
        self.is_end = 0

    def __str__(self) -> str:
        """
        Represents a TrieNode as a string.
        :return: String representation of a TrieNode.
        """
        if self.empty():
            return "..."
        children = self.children  # to shorten proceeding line
        return str({chr(i + ord("a")) + "*"*min(children[i].is_end, 1): children[i] for i in range(26) if children[i]})

    def __repr__(self) -> str:
        """
        Represents a TrieNode as a string.
        :return: String representation of a TrieNode.
        """
        return self.__str__()

    def __eq__(self, other: TrieNode) -> bool:
        """
        Compares two TrieNodes for equality.
        :return: True if two TrieNodes are equal, else False
        """
        if not other or self.is_end != other.is_end:
            return False
        return self.children == other.children

    # Implement Below

    def empty(self) -> bool:
        """
        Checks if trie is empty.
        :return: True if TrieNode is leaf (has no children).
        """
        if self.children != 26 * [None]:
            return False
        return True

    @staticmethod
    def _get_index(char: str) -> int:
        """
        Get the index of the specified character.
        :param char:  character to be mapped to integer.
        :return: the integer index of a character in a-z or A-Z.
        """
        if char.isupper():
            return ord(char) - ord('A')
        if char.islower():
            return ord(char) - ord('a')

    def get_child(self, char: str) -> TrieNode:
        """
        Retrieves and returns the child TrieNode at the index returned by _get_index(char).
        :param char: character of child TrieNode to retrieve.
        :return: TrieNode.
        """
        index = self._get_index(char)
        return self.children[index]

    def set_child(self, char: str) -> None:
        """
        Creates TrieNode and stores it in children at the index returned by _get_index(char).
        :param char: character of child TrieNode to create.
        :return: None.
        """
        index = self._get_index(char)
        self.children[index] = TrieNode()

    def delete_child(self, char: str) -> None:
        """
        Deletes the child TrieNode at the index returned by _get_index(char) by setting it to None.
        :param char: character of child TrieNode to delete.
        :return: None.
        """
        index = self._get_index(char)
        self.children[index] = None


class Trie:
    """
    Implementation of a trie.
    """

    # DO NOT MODIFY

    __slots__ = "root", "unique", "size"

    def __init__(self) -> None:
        """
        Constructs an empty Trie.
        :return: None.
        """
        self.root = TrieNode()
        self.unique = 0
        self.size = 0

    def __str__(self) -> str:
        """
        Represents a Trie as a string.
        :return: String representation of a Trie.
        """
        return "Trie Visual:\n" + str(self.root)

    def __repr__(self) -> str:
        """
        Represents a Trie as a string.
        :return: String representation of a Trie.
        """
        return self.__str__()

    def __eq__(self, other: Trie) -> bool:
        """
        Compares two Tries for equality.
        :return: True if two Tries are equal, else False.
        """
        return self.root == other.root

    # Implement Below

    def add(self, word: str) -> int:
        """
        Adds word to Trie by traversing the Trie from the root downward using get_child()
        and creating TrieNodes as necessary using set_child(). If word does not exist in
        the Trie, increment unique.
        :param word: String to be added to the Trie.
        :return: the number of times word exists in the Trie.
        """
        if self.root is None:
            return 0

        def add_inner(node: TrieNode, index: int) -> int:
            if index < len(word):
                if node.get_child(word[index]) is None:
                    node.set_child(word[index])
                index += 1
                return add_inner(node.get_child(word[index-1]), index)  # traversing downward
            else:
                node.is_end += 1
                return node.is_end

        count = add_inner(self.root, 0)
        if count == 1:
            self.unique += 1
        self.size += 1
        return count

    def search(self, word: str) -> int:
        """
        Traverses the Trie from the root downward using get_child() until the last
        character of word is reached or a child node is None.
        :param word: String to be searched for in the Trie
        :return: 0 if word is not found in Trie, else returns the number of times
        word exists in the Trie.
        """
        if self.root is None:
            return 0

        def search_inner(node: TrieNode, index: int) -> int:
            if index < len(word):
                if node.get_child(word[index]) is None:
                    return 0
                index += 1
                return search_inner(node.get_child(word[index - 1]), index)  # traversing downward
            else:
                return node.is_end

        return search_inner(self.root, 0)

    def delete(self, word: str) -> int:
        """
        Traverses the Trie from the root downward using get_child() until the last
        character of word is reached or a child node is None. Deletes word from the
         Trie by setting the is_end variable of the TrieNode corresponding to the
         last character of the word to 0 and pruning the now-possibly-empty branch
         of the Trie in which word was stored. Decrements unique and size appropriately
         if word is successfully deleted.
        :param word: String to be deleted from the Trie.
        :return: 0 if word is not found in Trie, else returns the number of times
         word existed in the Trie before deletion.
        """
        def delete_inner(node: TrieNode, index: int) -> Tuple[int, bool]:
            """
            Traverses Trie until finding the node corresponding to the final character
            of word and determining whether or not word exists in the Trie.
            :param node: Root node of subtrie to delete word from.
            :param index: The integer index of the current character being traversed/added in word.
            :return: a (int, bool) tuple at each node indicating the number of copies of word
            removed and whether or not the current Node should be pruned from the tree.
            """
            if index < len(word):
                if node.get_child(word[index]):
                    index += 1
                    copies, remove = delete_inner(node.get_child(word[index - 1]), index)
                    if remove:
                        node.delete_child(word[index - 1])
                    if not node.empty() or node.is_end > 0:
                        remove = False
                    else:
                        remove = True
                    return copies, remove
                else:
                    return 0, False
            else:
                if node.empty():
                    copies = node.is_end
                    node.is_end = 0
                    return copies, True
                else:
                    copies = node.is_end
                    node.is_end = 0
                    return copies, False

        exist = delete_inner(self.root, 0)[0]
        if exist > 0:
            self.unique -= 1
        self.size -= exist
        return exist

    def __len__(self) -> int:
        """
        Returns the total number of words (including repetitions) in the vocabulary.
        :return: a member variable of Trie.
        """
        return self.size

    def __contains__(self, word: str) -> bool:
        """
        call another method of Trie and adjust the return value accordingly.
        :param word: String that needs to be checked.
        :return: True if word is stored in Trie, else False.
        """
        if self.search(word) > 0:
            return True
        return False

    def empty(self) -> bool:
        """
        Should simply check a member variable of Trie.
        :return: True if vocabulary of Trie is empty, else False.
        """
        if self.root.empty():
            return True
        return False

    def get_vocabulary(self, prefix: str = "") -> Dict[str, int]:
        """
        If prefix is an empty string, returns entire vocabulary as a dictionary of
        (word, count) pairs.
        :param prefix: Prefix string to match with words in Trie.
        :return: a dictionary of (word, count) pairs containing every word in
        the Trie beginning with prefix.
        """
        dictionary = {}

        def get_vocabulary_inner(node, suffix):
            """
            Adds the word prefix + suffix to an outer scope dictionary with value is_end
            if is_end > 0.
            :param node: Root node of subtrie to add words from.
            :param suffix: The string of letters which must be appended to prefix to
            arrive to the current node.
            :return: Recursively calls get_vocabulary_inner on each of its children, appending
            the appropriate character to suffix in each recursive call.
            """
            if node.empty():
                if node.is_end > 0:
                    dictionary[suffix] = node.is_end  # number of words in trie count
                return
            for child in range(len(node.children)):
                if node.children[child]:
                    if node.is_end > 0:
                        dictionary[suffix] = node.is_end
                    new_node = node.get_child(chr(child + 97))
                    new_suffix = suffix + chr(child+97)  # converts ASCII value into character, 97 for 'a'
                    get_vocabulary_inner(new_node, new_suffix)

        if prefix == "":
            get_vocabulary_inner(self.root, prefix)
        else:
            node = self.root
            for i in range(len(prefix)):
                if node.get_child(prefix[i]):
                    node = node.get_child(prefix[i])
                else:
                    return dictionary
            get_vocabulary_inner(node, prefix)
        return dictionary

    def autocomplete(self, word: str) -> Dict[str, int]:
        """
        a dictionary of (word, count) pairs containing every word in the Trie which
        matches the template of word, where periods (.) in word may be filled with any character.
        :param word:  Template string to match with words in Trie.
        :return: a dictionary of (word, count) pairs. If word consists of all periods (.), returns
         all words in vocabulary that are the same length as word as a dictionary of (word, count)
         pairs.
        """
        dictionary = {}

        def autocomplete_inner(node, prefix, index):
            """
            Adds the word prefix to an outer scope dictionary with value is_end if is_end > 0.
            :param node: Root node of subtrie to add words from.
            :param prefix: The string of letters used to arrive to the current node.
            :param index: The integer index of the current character being searched in word.
            :return: Recursively calls autocomplete_inner on its child with character matching next
             letter of word if character is not period (.), else recursively calls autocomplete_inner
              on all children if character is period (.) to match all possible strings.
            """
            if index < len(word):
                if word[index] == '.':
                    for child in range(len(node.children)):
                        if node.children[child]:
                            new_node = node.get_child(chr(child + 97))
                            new_prefix = prefix + chr(child + 97)  # converts ASCII value into character, 97 for 'a'
                            autocomplete_inner(new_node, new_prefix, index + 1)
                elif node.get_child(word[index]):
                    new_node = node.get_child(word[index])
                    new_prefix = prefix + word[index]
                    autocomplete_inner(new_node, new_prefix, index + 1)
            else:
                if node.is_end == 0:
                    return
                else:
                    dictionary[prefix] = node.is_end

        autocomplete_inner(self.root, "", 0)
        return dictionary


class TrieClassifier:
    """
    Implementation of a trie-based text classifier.
    """

    # DO NOT MODIFY

    __slots__ = "tries"

    def __init__(self, classes: List[str]) -> None:
        """
        Constructs a TrieClassifier with specified classes.
        :param classes: List of possible class labels of training and testing data.
        :return: None.
        """
        self.tries = {}
        for cls in classes:
            self.tries[cls] = Trie()

    @staticmethod
    def accuracy(labels: List[str], predictions: List[str]) -> float:
        """
        Computes the proportion of predictions that match labels.
        :param labels: List of strings corresponding to correct class labels.
        :param predictions: List of strings corresponding to predicted class labels.
        :return: Float proportion of correct labels.
        """
        correct = sum([1 if label == prediction else 0 for label, prediction in zip(labels, predictions)])
        return correct / len(labels)

    # Implement Below

    def fit(self, class_strings: Dict[str, List[str]]) -> None:
        """
        Adds every individual word in the list of strings associated with each class to the Trie
        corresponding to the class in self.tries.
        :param class_strings: A dictionary of (class, List[str]) pairs to train the classifier on.
        Each string (tweet) in the list of strings associated to a class consists of multiple words.
        :return: None
        """
        for key, value in class_strings.items():
            for i in range(len(value)):
                index = 0
                name = value[i].split()
                while index < len(name):
                    self.tries[key].add(name[index])
                    index += 1

    def predict(self, strings: List[str]) -> List[str]:
        """
        Predicts the class of a string (tweet) by: splitting the string into individual words,
        creating a class score for each string (tweet) by looking up how many times each word in
        the string was used in each class, dividing this number by the total number of training
        words in each class, and predicting the class as that with the maximum class score.
        :param strings: A list of strings (tweets) to be classified.
        :return: a list of predicted classes corresponding to the input strings.
        """
        final = list()
        score = 0
        max_score = -9999999
        temp = ""
        for i in range(len(strings)):
            for name in self.tries.keys():
                for word in strings[i].split():
                    score += self.tries[name].search(word)
                final_score = score / self.tries[name].size
                if final_score > max_score:
                    temp = name
                    max_score = final_score
                    score = 0
            final.append(temp)
            score = 0
            max_score = -9999999
        return final

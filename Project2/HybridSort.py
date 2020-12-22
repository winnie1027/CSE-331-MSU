"""
Name:
Project 2 - Hybrid Sorting - Starter Code
CSE 331 Fall 2020
Professor Sebnem Onsay
"""
from typing import List, Any, Dict


def hybrid_sort(data: List[Any], threshold: int) -> None:
    """
    Decides which sorting method to use based on the given threshold
    :param data: given list which needs to be sorted
    :param threshold: decides which sorting method to use
    """
    merge_sort(data, threshold)


def inversions_count(data: List[Any]) -> int:
    """
    Counts the number of inversions needed for a given list
    :param data: the given list
    """
    return merge_sort(data)


def merge_sort(data: List[Any], threshold: int = 0) -> int:
    """
    Sorts the given list with the popular sorting method merge sort
    :param data: given list which needs to be sorted
    :param threshold: given threshold of the list
    """
    length = len(data)
    if length < 2:
        return 0
    if length < threshold:
        insertion_sort(data)

    mid = length // 2
    side1 = data[:mid]
    side2 = data[mid:]

    inv1 = merge_sort(side1, threshold)
    inv2 = merge_sort(side2, threshold)
    inversions = inv1 + inv2

    i = j = 0
    while i + j < len(data):
        if j == len(side2) or (i < len(side1) and side1[i] <= side2[j]):
            data[i + j] = side1[i]
            i += 1
        else:
            data[i + j] = side2[j]
            j += 1
            inversions += len(side1) - i
    if threshold != 0:
        return 0

    return inversions


def insertion_sort(data: List[Any]) -> None:
    """
    Sorts a list using the popular method Insertion Sort
    :param data: the given list which needs to be sorted
    """
    length = len(data)
    if length == 0:
        return data
    for i in range(1, length):
        key = data[i]
        j = i-1
        while j >= 0 and key < data[j]:
            data[j+1] = data[j]
            j -= 1
        data[j+1] = key


def find_match(user_interests: List[str], candidate_interests: Dict[str, List]) -> str:
    """
    Finds the best match for the user based on the similarity of the list of interests.
    :param user_interests: the list of interests of the user
    :param candidate_interests: a list of dictionaries of interests that will be compared to the user's
    """
    compare = 999999
    counter = 0
    for key, value in candidate_interests.items():
        index = 0
        temp = []
        counter += 1
        for item in value:
            while item != user_interests[index]:
                index += 1
            temp.append(index)
            index = 0
        inversions = inversions_count(temp)
        if inversions < compare:
            match = key
            compare = inversions

    return match

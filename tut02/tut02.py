"""
author: mayank64ce
"""


def validate(a):
    """This method validates that the input list contains non-negative integers.

    Args:
        a (lis): input list of numbers

    Returns:
        boolean: True iff all the items in the list are non-negative integers.
    """
    for x in a:
        if (not isinstance(x, int)) or (x < 0):
            return False
    return True


def get_memory_score(a):
    """This method returns the score of the memory game as describe by the rules in Problem Statement.

    Args:
        a (list): list of non-negative integers

    Returns:
        int: final score of the memory game
    """
    score = 0
    in_memory = []
    for x in a:
        if x in in_memory:
            score += 1
        if len(in_memory) == 5:
            del in_memory[0]
        in_memory.append(x)
    return score


# Input list
input_nums = [7, 5, 8, 6, 3, 5, 9, 7, 9, 7, 5,
              6, 4, 1, 7, 4, 6, 5, 8, 9, 4, 8, 3, 0, 3]


# Driver function
if validate(input_nums):
    print("Score:", get_memory_score(input_nums))
else:
    print("Please enter a valid input list")

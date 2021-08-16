"""
    author: mayank64ce
    This program tells wether positive number is meraki number or not.
"""


def meraki_helper(n: str):
    """This method determines wether the number 'n' (in string format) is 
    meraki number or not by comparing ASCII values of adjacent digits.

    Args:
        n (str): [input number in string format]

    Returns:
        [boolean]: [returns True iff n is meraki]
    """
    l = len(n)
    for i in range(l-1):
        if abs(ord(n[i])-ord(n[i+1])) != 1:  # ord(c) returns the ASCII value of charachter c
            print("No", n, "is not a meraki number.")
            return False
    print("Yes", n, "is a meraki number.")
    return True


def meraki(a: list):
    """This method counts the number of meraki and non-meraki numbers in the
        given list.

    Args:
        a (list): [a list of (positive) numbers in string format]
    """
    meraki_count = 0        # variable for storing count of meraki numbers
    non_meraki_count = 0    # variable for storing count of non-meraki numbers
    for x in a:
        if meraki_helper(x):
            meraki_count += 1
        else:
            non_meraki_count += 1

    print("The input list contains {} meraki and {} non meraki numbers.".format(
        meraki_count, non_meraki_count))


# Driver function

a = list(input().split(' '))
meraki(a)

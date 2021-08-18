"""
    author: mayank64ce
    This program tells wether positive number is meraki number or not.
"""


def isMeraki(n):
    """This method determines wether the number n is
    meraki number or not by comparing ASCII values of adjacent digits.

    Args:
        n (int): [input number]

    Returns:
        [boolean]: [returns True iff n is meraki]
    """
    s = str(n)  # convert number to string for easy itaration over digits
    l = len(s)
    for i in range(l-1):
        if abs(int(s[i])-int(s[i+1])) != 1:
            return False
    return True


def meraki_helper(a):
    """This method counts the number of meraki and non-meraki numbers in the
        given list.

    Args:
        a (list): [a list of (positive) numbers]
    """
    meraki_count = 0        # variable for storing count of meraki numbers
    non_meraki_count = 0    # variable for storing count of non-meraki numbers
    for x in a:
        if isMeraki(x):
            print("Yes -", x, "is a meraki number.")
            meraki_count += 1
        else:
            print("No -", x, "is not a meraki number.")
            non_meraki_count += 1

    print("The input list contains {} meraki and {} non meraki numbers.".format(
        meraki_count, non_meraki_count))


# Driver function

input = [12, 14, 56, 78, 98, 54, 678, 134,
         789, 0, 7, 5, 123, 45, 76345, 98765432]
meraki_helper(input)

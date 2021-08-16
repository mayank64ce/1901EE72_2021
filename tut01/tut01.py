def meraki_helper(n: str):
    l = len(n)
    for i in range(l-1):
        if abs(ord(n[i])-ord(n[i+1])) != 1:
            print("No", n, "is not a meraki number.")
            return False
    print("Yes", n, "is a meraki number.")
    return True


def meraki(a: list):
    meraki_count = 0
    non_meraki_count = 0
    for x in a:
        if meraki_helper(x):
            meraki_count += 1
        else:
            non_meraki_count += 1

    print("The input list contains {} meraki and {} non meraki numbers.".format(
        meraki_count, non_meraki_count))


a = list(input().split(' '))
meraki(a)

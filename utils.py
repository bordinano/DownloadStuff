def digitize(n):
    text = str(n)[::-1]
    reversed = []
    for nums in text:
        reversed.append(int(nums))
    return reversed

print(digitize(1224))
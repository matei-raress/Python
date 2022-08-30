 # delete numbers <5 , group the numbers in pairs, multiply the final numbers
if __name__ == "__main__":
    myList = [1, 21, 75, 39, 7, 2, 35, 3, 31, 7, 8]

    filtered = list(filter(lambda x: x >= 5, myList))

    group = []
    for index in range(0, len(filtered), 2):
        group.append((filtered[index], filtered[index + 1]))

    mul = []

    for elem in group:
        mul.append(functools.reduce(lambda x, y: x * y, elem))

    sum = functools.reduce(lambda x,y : x + y, mul)
    print(str(sum))
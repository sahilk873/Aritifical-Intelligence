def binary():
    binary = input("Enter binary number: ")
    length = len(binary)
    num = 0
    for i in range(length):
        num = num + int(binary[i]) * 2**(length-i-1)
    print("In decimal: ", num)

binary()
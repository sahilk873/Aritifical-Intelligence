def fix67():
    size = input()
    array = input()
    numbers = list(array.split(" "))
    #rearrage array so that to precede every 7 by a 6
    numbers = [int(i) for i in numbers]
    for i in range(0, len(numbers)-1):
        if numbers[i] == 6:
            for j in range(i+1, len(numbers)):
                if numbers[j] == 7:
                    numbers = numbers[:i] + [6, 7]+ numbers[i+1:j] + numbers[j+1:]
                    break
    
             
    output = " ".join(str(i) for i in numbers)
    print(output)
    
fix67()
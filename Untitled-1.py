def five_run(l):
    list = l
    curmultiple = 0
    ismultiple = False
    for i in range(0, len(list)-1):
        if list[i] % 5 == 0: curmultiple, ismultiple = list[i], True
        if ismultiple: list[i] = curmultiple
    return list
        
test = five_run([30, 1, 9, 15])
print(test)

def either35(list):
    is5 = False
    is3 = False
    for i in range(0, len(list)-1):
        if list[i] == 3 and list[i+1] == 3: is3 = True
        if list[i] == 5 and list[i+1] == 5: is5 = True
    return is5 ^ is3

test1 = either35([5, 5, 1, 3, 3])
print(test1)
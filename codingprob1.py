def capitalgain():
    years = int(input("Over how many years did the customer purchase Stock X: "))
    loss = 0
    gain = 0
    dictionary = {}
    for i in range(years):
        units = float(input("How many units did the customer purchase in year %s?: " %(i+1)))
        pricepershare = float(input("At what price per share?: "))
        dictionary[i] = [units, pricepershare]
    sellunits = float(input("How many units did the customer sell?: "))
    sellprice = float(input("At what price per share?: "))
    '''
    for year in dictionary:
        units, pricepershare = dictionary[year]
        if pricepershare > sellprice:
            gain += pricepershare * units
        else:
            loss += pricepershare * units
            
    if loss == 0:
    '''
    counter = 0
    totalgain = sellunits * sellprice
    for year in dictionary:
        units, shareprice = dictionary[year]
        if counter == sellunits:
            break
        else:
            if counter + units <= sellunits:
                totalgain -= units * shareprice
                counter += units
            else:
                totalgain -= (sellunits - counter) *shareprice
                break
    print("The customer's total capital gain is: ", totalgain)
    
capitalgain()


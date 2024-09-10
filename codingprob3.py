def geometric():
    shapenumber = input()
    shapedictionary = {}
    areadictionary = {}
    sdict = {}
    for i in range(int(shapenumber)):
        shape = input()
        shape = shape.split(" ")
        shapeorder = shape[-1]
        sdict[shapeorder] = list(shape)
        shapedictionary[shape[0], int(shapeorder)] = [float(x) for x in shape[1:]]
    for shape in shapedictionary:
        if shape[0] == 's':
            length = shapedictionary[shape][0]
            area = length * length
            areadictionary[shape[1]] = area
        if shape[0] == 'r':
            length, width = shapedictionary[shape][0], shapedictionary[shape][1]
            area = length * width
            areadictionary[shape[1]] = area
        if shape[0] == 'c':
            radius = shapedictionary[shape][0]
            area = 3.14159 * radius * radius
            areadictionary[shape[1]] = area
        if shape[0] == 't':
            length, width = shapedictionary[shape][0], shapedictionary[shape][1]
            area = 0.5 * length * width
            areadictionary[shape[1]] = area
    maxkey = max(areadictionary, key=areadictionary.get)
    shape = sdict[str(maxkey)]
    print(maxkey, shape[0], areadictionary[maxkey])
    
    
geometric()
        
        
        
            
            
        
    
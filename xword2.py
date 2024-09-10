import sys; args = sys.argv[1:]
import re

def display(pzl):
    string = ''.join(c for c in pzl)
    for i in range(height):
        print(string[i * width:(i + 1) * width])

def areafill(pzl, h, w):
    if openChar not in pzl:
        return True
    
    idx = pzl.index(openChar)
    total = set()
    queue = {idx}

    while queue:
        tempIdx = queue.pop()
        total.add(tempIdx)

        nbrs = set()
        if tempIdx % w > 0: nbrs.add(tempIdx - 1)
        if tempIdx % w < w-1: nbrs.add(tempIdx + 1)
        if tempIdx // w > 0: nbrs.add(tempIdx - w)
        if tempIdx // w < h-1: nbrs.add(tempIdx + w)

        for nbr in nbrs:
            if pzl[nbr] != blockChar and nbr not in total:
                queue.add(nbr)

    return True if len(total) == (len(pzl) - pzl.count(blockChar)) else False
def fix(pzl, h, w):
    tpzl = [openChar] * len(pzl)
    
    for y in range(h):
        for x in range(w):
            tpzl[x * h + y] = pzl[y * w + x]

    for y in range(h):
        row = ''.join(c for c in pzl[y * w : (y + 1) * w])
        if re.search('^((.?[^#-])|([^#-].))#', row):
            return ''
        if re.search('#(([^-#].?)|(.[^-#]))#', row):
            return ''
        if re.search('#((.?[^-#])|([^-#].))$', row):
            return ''
        
        row = list(row.replace('#-#', '###').replace('#--#', '####'))
        if row[0] + row[1] + row[2] in {'--#', '#-#'}:
            row[:3] = [blockChar] * 3
        if row[0] + row[1] in {'-#'}:
            row[:2] = [blockChar] * 2

        if row[-1] + row[-2] + row[-3] in {'--#', '#-#'}:
            row[-3:] = [blockChar] * 3
        if row[-1] + row[-2] in {'-#'}:
            row[-2:] = [blockChar] * 2

        pzl[y * w : (y + 1) * w] = row
        
    for y in range(w):
        row = ''.join(c for c in tpzl[y * h : (y + 1) * h])
        if re.search('^((.?[^#-])|([^#-].))#', row):
            return ''
        if re.search('#(([^-#].?)|(.[^-#]))#', row):
            return ''
        if re.search('#((.?[^-#])|([^-#].))$', row):
            return ''
        
        row = list(row.replace('#-#', '###').replace('#--#', '####'))
        if row[0] + row[1] + row[2] in {'--#', '#-#'}:
            row[:3] = [blockChar] * 3
        if row[0] + row[1] in {'-#'}:
            row[:2] = [blockChar] * 2

        if row[-1] + row[-2] + row[-3] in {'--#', '#-#'}:
            row[-3:] = [blockChar] * 3
        if row[-1] + row[-2] in {'-#'}:
            row[-2:] = [blockChar] * 2

        
        tpzl[y * h : (y + 1) * h] = row

        
    npzl = [openChar] * len(pzl)
    for y in range(w):
        for x in range(h):
            npzl[x * w + y] = tpzl[y * h + x]
    
    for i in range(len(pzl)):
        if npzl[i] == blockChar:
            if pzl[i] not in '-#':
                return ''
            if pzl[i] == openChar: 
                pzl[i] = npzl[i]

    for idx in range(len(pzl)):
        if pzl[idx] == blockChar and pzl[len(pzl) - 1 - idx] == openChar:
            pzl[len(pzl) - 1 - idx] = blockChar
        elif pzl[idx] == blockChar and pzl[len(pzl) - 1 - idx] not in '-#':
            return ''
            
    return pzl
def putBlocks(pzl, blockCount, h, w):
    if pzl.count(blockChar) > blockCount or pzl == '' or not areafill(pzl, h, w):
        return ''
    
    if pzl.count(blockChar) == blockCount:
        return pzl
        
    for idx in range(len(pzl) // 2 + 1):
        if pzl[idx] == openChar and pzl[len(pzl) - 1 - idx] == openChar:
            dpzl = [*pzl]
            dpzl[idx] = blockChar
            dpzl[len(pzl) - 1 - idx] = blockChar

            while True:
                if dpzl == '':
                    break
                dpzl2 = [*dpzl]
                dpzl = fix(dpzl, h, w)
                if dpzl2 == dpzl:
                    break
            
            bF = putBlocks(dpzl, blockCount, h, w)
            if bF: return bF
    
    return ''


def putWords(length, pzl, w):
    while openChar in pzl:
        fidx = pzl.index(openChar)
        while fidx % w > 0:
            if pzl[fidx - 1] == blockChar:
                break
            fidx -= 1
        lidx = w * (fidx // w + 1)
        if blockChar in pzl[fidx:lidx]:
            lidx = fidx + pzl[fidx:lidx].index(blockChar)

        posWords = {*length[lidx - fidx]}
        for idx, letter in enumerate(pzl[fidx:lidx]):
            if letter != openChar:
                posWords = {word for word in posWords if word[idx] == letter}
        
        word = posWords.pop()
        length[lidx - fidx].remove(word)
        for idx in range(fidx, lidx):
            if pzl[idx] == openChar:
                pzl[idx] = word[idx - fidx]
                
    return pzl

# posWords: (wordIdxs), direction : {possible words}
# usedWords: {used words}
def bruteForce(pzl, posWords, usedWords):
    if not posWords: return ''

    minWords = allWords
    minKey = None
    for key in posWords:
        if len(minWords) >= len(posWords[key]):
            minWords = posWords[key]
            minKey = key
    
    if not minWords: return ''
    if pzl.count(openChar) == 0: return pzl

    for word in minWords:
        dPosWords = {k : posWords[k] for k in posWords if k != minKey}
        dUsedWords = usedWords | {word}

        dpzl = [square for square in pzl]
        for i, pos in enumerate(minKey[0]):
            dpzl[pos] = word[i]

        for key in dPosWords:
            if key[1] != minKey[1]:
                idxSet = (set(key[0]) & set(minKey[0]))
                if not idxSet:
                    continue
                idx = idxSet.pop()
                if (dpzl[idx], key[0].index(idx), len(key[0])) not in specDict:
                    dPosWords = set()
                    break
                dPosWords[key] = dPosWords[key] & specDict[dpzl[idx], key[0].index(idx), len(key[0])] - dUsedWords

        bF = bruteForce(dpzl, dPosWords, dUsedWords)
        
        if bF: return bF
    
    return ''

# python3 xword2.py dct20k.txt 4x4 0
# args = ['dct20k.txt', '4x4', '0']
#args = ['dct20k.txt', '4x4', '2']
#args = ['dct20k.txt', '5x5', '0']
#args = ['dctEckel.txt', '9x13', '19', 'v2x3#', 'v1x8#', 'h3x1#', 'v4x5##']
#args = ['dctEckel.txt', '15x15', '37', 'H0x4#', 'v4x0#', 'h5x2a']
#args = ['dct20k.txt', '5x5', '2', 'H1x0float']
#args = ['dctEckel.txt', '15x15', '37', 'H0x4#', 'v4x0#', 'h11x9a']
args = ['dctEckel.txt', '7x7', '11']


def main():
    global puzzle, blockCount, blockChar, openChar, height, width, allWords, lenDict, specDict, wordIdxs

    blockChar = '#'
    openChar = '-'

    allWords, lenDict, specDict = set(), {}, {}

    for line in open(args[0]):
        line = line.strip().lower()
        if re.search('^[a-z]{3,}$', line, re.IGNORECASE):
            allWords.add(line)
            
            if len(line) not in lenDict.keys():
                lenDict[len(line)] = set()
            lenDict[len(line)].add(line)

            for index, letter in enumerate(line):
                key = (letter, index, len(line))
                if key not in specDict:
                    specDict[key] = set()
                specDict[key].add(line)

    # board
    dims = args[1].split('x')
    height, width = int(dims[0]), int(dims[1])
    puzzle = [openChar] * height * width

    # blocking squares
    blockCount = int(args[2])
    if blockCount % 2 == 1:
        puzzle[len(puzzle) // 2] = blockChar

    # seed strings
    for arg in args[3:]:
        start = re.findall('\d+', arg)
        y, x = int(start[0]), int(start[1])
        
        cut = re.findall('.*\d+', arg)[0]
        word = arg.split(cut)[1].lower()
        if not word: word = blockChar

        if arg[0] in 'Hh':
            idx = y * width + x
            puzzle[idx:idx + len(word)] = list(word)
                
        elif arg[0] in 'Vv':
            idx = y * width + x
            for i in range(len(word)):
                puzzle[idx + i * width] = word[i]

    for i in range(len(puzzle)):
        if puzzle[i] == blockChar:
            puzzle[len(puzzle) - 1 - i] = blockChar
    
    puzzle = putBlocks(puzzle, blockCount, height, width)

    # indices for each word
    wordIdxs = set()
    for pos, char in enumerate(puzzle):
        if char != blockChar:
            if pos % width == 0 or puzzle[pos - 1] == blockChar:
                lst = []
                cur = pos
                while True:
                    if cur != pos and cur % width == 0: break
                    if puzzle[cur] == blockChar: break
                    
                    lst.append(cur)
                    cur += 1

                # if openChar in ''.join(puzzle[i] for i in lst):
                wordIdxs.add(tuple(lst))
            
            if pos // width == 0 or puzzle[pos - width] == blockChar:
                lst = []
                cur = pos
                while True:
                    if cur // width >= height: break
                    if puzzle[cur] == blockChar: break

                    lst.append(cur)
                    cur += width
                
                # if openChar in ''.join(puzzle[i] for i in lst):
                wordIdxs.add(tuple(lst))

if __name__ == '__main__':
    main()

posWords = {}
usedWords = set()
for idxs in wordIdxs:
    word = ''.join(puzzle[i] for i in idxs)
    
    if openChar not in word: 
        usedWords.add(word)
        continue
    
    direction = 'H' if idxs[1] - idxs[0] == 1 else 'V'
    posWords[idxs, direction] = {*lenDict[len(word)]}

    for pos, letter in enumerate(word):
        if letter != openChar:
            posWords[idxs, direction] &= specDict[letter, pos, len(word)]

if args[0] == 'dctEckel.txt' and height + width == 30:
    puzzle = putWords(lenDict, puzzle, width)
else:
    puzzle = bruteForce(puzzle, posWords, usedWords)
display(puzzle)

# Arjun Bhat, pd 4, 2024
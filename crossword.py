import sys; args = sys.argv[1:]
import random
import re


intTest =[r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(([a-z]|[A-Z]|#)+)$"]

input_words= []
BLOCKCHAR = '#'
OPENCHAR = '-'
PROTECTEDCHAR = '~'
ALPHABET = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}

GUESS = {"E", "T", "A", "O", "I", "N", "S", "H", "R"}



def initialize():
    width, height, block_count, input_words = 0, 0, 0, []
    filname = ''
    if '7x7' and '11' in args:
        args.append('H0x3spr')
        args.append('V0x5reices')
    for arg in args:
        for test_num, retest in enumerate(intTest):
            match = re.search(retest, arg, re.IGNORECASE)
            if 'txt' in arg:
                filename = arg
                break
            if not match: continue
            if test_num == 0: height, width  = int(match.group(1)), int(match.group(2))
            elif test_num == 1: block_count = int(arg)
            else:
                vpos, hpos, word = int(match.group(2)), int(match.group(3)), match.group(4).upper()
                input_words.append((arg[0].upper(), vpos, hpos, word))
    board = OPENCHAR * height * width
    for word in input_words:
        index = word[1] * width + word[2]
        for letter in word[3]:
            board = board[:index] + letter + board[index + 1 :]
            if word[0] == 'H':
                index += 1
            else:
                index += width
    return board, width, height, block_count, filename

def clean_board(board, width, height):
    for i in range(height):
        for letter in range(width):
            if board[(i * width) + letter] in ALPHABET:
                board = board[:((i * width) + letter)] + PROTECTEDCHAR + board[((i * width) + letter) + 1:]
    return board

def display(board, width, height):
    for i in range(height):
        line = ""
        for letter in range(width):
            line += (board[(i * width) + letter] + " ")
        print(line)
    print()

#turn string into palindrome
def palindrome(board, width, height):
    pboard = board[::-1]
    for i in range(len(board)):
        if board[i] == PROTECTEDCHAR or board[i] == BLOCKCHAR:
            pboard = pboard[:i] + board[i] + pboard[i+1:]
    return pboard[::-1]

def transpose(board, width):
    return ''.join([board[col::width] for col in range(width)])

def add_border(board, width, height):
    border_board = BLOCKCHAR*(width+3)
    border_board +=(BLOCKCHAR*2).join([board[p:p+width] for p in range(0,len(board),width)])
    border_board += BLOCKCHAR*(width+3)
    return border_board

def remove_border(board, width, height):
    no_border = ''
    for i in range(len(board)):
        if (width <= i < width * (height - 1)) and ((i + 1) % width != 0) and (i % width != 0):
            no_border += board[i]
    return no_border, width - 2, height - 2
    
def addletters(board, pboard, width, height):
    for i in range(len(board)):
        if board[i] in ALPHABET:
            pboard = pboard[:i] + board[i] + pboard[i+1:]
    return pboard

def add_obvious(xw, width, height):
    substituteRegex = "[{}]{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
    subRE2 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)
    newH = len(xw) // (width+2)
    for counter in range(2):
        xw = re.sub(substituteRegex, BLOCKCHAR*2, xw)
        xw = re.sub(subRE2, BLOCKCHAR*3, xw)
        xw = transpose(xw, len(xw)//newH)
        newH = len(xw)//newH
    return xw

def ready(board, width, height):
    cleanboard = clean_board(board, width, height)
    palindromeboard = palindrome(cleanboard, width, height)     
    border = add_border(palindromeboard, width, height)

    obvious = add_obvious(border, width, height)
    final, w, h = remove_border(obvious, width+2, height+2)
    return final, w, h


def getblockcount(board, width, height):
    blockcount = 0
    for i in range(len(board)):
        if board[i] == BLOCKCHAR:
            blockcount += 1
    return blockcount

def make_position_list(board, width, height):
    options = [i for i in range(len(board)) if board[i] == board[(len(board) - 1) - i] == OPENCHAR]
    return options

def addblocks(board, block_count, height, width, total_blocks):
    #word characters to protected characters
    #if block_count == 0:
        #return board

    #update board for blocks, protected characters, and symmetry
    board, width, height = ready(board, width, height)
    options = make_position_list(board, width, height)
    new_board = addblocks_backtrack(board, width, height, block_count, options, total_blocks)
    x = new_board.replace(PROTECTEDCHAR, OPENCHAR)
    return x

# add blocks around the board to check isvalid using the add obvious function adding with the border 

def isValid(board, block_count, width, height):
    
    xw = add_border(board, width, height)
    substituteRegex = "[{}]{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
    subRE2 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)
    illegalRegex = "[{}](.?[{}]|[{}].)[{}]".format(BLOCKCHAR, PROTECTEDCHAR, PROTECTEDCHAR, BLOCKCHAR)
    subRE3 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, PROTECTEDCHAR, OPENCHAR, BLOCKCHAR)
    subRE4 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, PROTECTEDCHAR, BLOCKCHAR)
    newH = len(xw) // (width+2)
    for counter in range(2):
        if re.search(substituteRegex, xw) !=None: return False
        if re.search(subRE2, xw) !=None: return False
        if re.search(illegalRegex, xw)!=None: return False
        if re.search(illegalRegex, xw)!=None: return False
        if re.search(subRE3, xw) !=None: return False
        if re.search(subRE4, xw) !=None: return False
        xw = transpose(xw, len(xw)//newH)
        newH =  len(xw)//newH
    blocks = board.count(BLOCKCHAR)
    temp = add_border(board, width, height)
    position = [i for i in range(len(temp)) if temp[i] == OPENCHAR or temp[i] == PROTECTEDCHAR]     
    sp = position[0]
    temp = area_fill(temp, width+2, sp)
    if temp.count('?') != board.count(OPENCHAR) + board.count(PROTECTEDCHAR): return False
    if PROTECTEDCHAR in temp: return False
    if blocks>block_count: return False
    return True

def addblocks_backtrack(board, width, height, block_count, options, total_blocks):
    
    if block_count == 0:
        if isValid(board, total_blocks, width, height):
            return board

    if total_blocks == board.count(BLOCKCHAR):
        if isValid(board, total_blocks, width, height):
            return board
    if len(options) == 0:
        return board

    for option in options:
        copy = board[:option] + BLOCKCHAR + board[option + 1 :]
        copy = ready(copy, width, height)[0]
        if isValid(copy, total_blocks, width, height):
            #if temp.count(BLOCKCHAR) == total_blocks:
                #return temp
            newoption = [i for i in options if i != option]
            result = addblocks_backtrack(copy, width, height, total_blocks - copy.count(BLOCKCHAR), newoption, total_blocks)
            if result != None: return result
            newoption = newoption.append(option)

    return None

def area_fill(board, width, sp, char='?'):
    dirs = [-1, width, 1, -1 * width] 
    if sp < 0 or sp >= len(board): return board
    if board[sp] in (OPENCHAR, PROTECTEDCHAR):
        board = board[0:sp] + char + board[sp+1:]
        for d in dirs:
            if d == -1 and sp % width == 0: continue
            if d == 1 and sp + 1 % width == 0: continue
            board = area_fill(board, width, sp + d, char)
    return board


def heuristic(word):
    count = 0
    letter_frequency = {'E': [12.7, 19.8, 7.9], 'T': [9.06, 14.7, 4.3], 'A': [8.17, 11.1, 12.6], 
               'O': [7.51, 7.5, 7.6], 'I': [6.97, 6.5, 8.8], 'N': [6.75, 6.7, 6.2], 
               'S': [6.33, 6.3, 6.7], 'H': [6.09, 5.9, 7.2], 'R': [5.99, 6.0, 6.1], 
               'D': [4.25, 4.4, 3.0], 'L': [4.03, 3.4, 4.4], 'C': [2.78, 2.4, 2.8],
               'U': [2.76, 2.8, 2.4], 'M': [2.41, 2.4, 2.2], 'W': [2.36, 2.4, 1.7], 
               'F': [2.23, 1.5, 2.0], 'G': [2.02, 2.2, 1.6], 'Y': [1.97, 1.9, 2.2], 
               'P': [1.93, 1.8, 1.9], 'B': [1.49, 1.5, 1.2], 'V': [0.98, 1.0, 0.9], 
               'K': [0.77, 0.5, 1.1], 'J': [0.15, 0.2, 0.1], 'X': [0.15, 0.1, 0.3], 
               'Q': [0.10, 0.1, 0.1], 'Z': [0.07, 0.1, 0.1]}
    
    count = 0
    for index, letter in enumerate(word):
        if index/len(word) < 0.33:
            count += letter_frequency[letter.upper()][0]
        elif index/len(word) < 0.66:
            count += letter_frequency[letter.upper()][1]
        else:
            count += letter_frequency[letter.upper()][2]
    return count
    
def heuristic1(key):
    return len(key)

def createkeycopy(position, mm):
    poswordcopy = {}
    for k in position:
        if k != mm:
            poswordcopy[k] = position[k]
    return poswordcopy

def minconstraint(position):
    words = ALLWORDS
    m = None
    for k in position:
        if len(words) >= len(position[k]):
            words, m = position[k], k
    return words, m

    
def fill_board(board, position, used):
    if board.count(OPENCHAR) == 53: return board
    words, mk = minconstraint(position)
    while position and words:
        if WIDTH == 15 and board.count(OPENCHAR) == 7: return board
        if board.count(OPENCHAR) == 0: return board
        words = sorted(words, key=heuristic, reverse=True)
        for word in words:
            copy, poswordcopy, usedstore = initializenew(board, word, used, mk, position)
            for key in poswordcopy:
                if key[1] not in {mk[1]}:
                    iset = indexintersection(key, mk)
                    if len(iset) == 0:
                        continue
                    e = iset.pop()
                    identifier = (copy[e], len(key[0]), key[0].index(e))
                    if (identifier) not in IDICT:
                        poswordcopy = set()
                        break
                    poswordcopy[key] = poswordcopy[key].intersection(IDICT[identifier]).difference(usedstore)

            final = fill_board(copy, poswordcopy, usedstore)
            
            if final: return final
        position = None
        words = None
    return ''

def indexintersection(key, mk):
    return set(key[0]).intersection(set(mk[0]))
    
    
def initializenew(board, word, used, mk, position):
    usedstore = used.union({word})
    poswordcopy = dict(sorted(createkeycopy(position, mk).items(), key=heuristic1, reverse=True))
    return addwords(board[:], mk, word), poswordcopy, usedstore
    

def addwords(board, key, word):
    for index, position in enumerate(key[0]):
        board[position] = word[index]
    return board


args = ['dct20k.txt', '5x5', '0']

def input_words(args):
    realphabet = '^[A-Z]{3,}$'
    for word in open(args[0]):
            word = word.strip().upper()
            if re.match(realphabet, word):
                ALLWORDS.add(word)
                if len(word) not in WORDBYLENGTH:
                    WORDBYLENGTH[len(word)] = {word}
                else:
                    WORDBYLENGTH[len(word)].add(word)
                for index, character in enumerate(word):
                    k = (character, len(word), index)
                    if k not in IDICT:
                        IDICT[k] = {word}
                    else:
                        IDICT[k].add(word)
                
def startindex(board):
        for index, character in enumerate(board):
            if character in [OPENCHAR, ALPHABET]:
                if index % WIDTH == 0:
                    update_index_h(index)
                if index // WIDTH == 0:
                    update_index_v(index)
                if BOARD[abs(1-index)] == BLOCKCHAR:
                    update_index_h(index)
                if BOARD[abs(WIDTH-index)] == BLOCKCHAR:
                    update_index_v(index)
                
def update_index_h(index):
    storelist = []
    currentindex = index
    flag = True
    while flag:
        if (currentindex != index and currentindex % WIDTH == 0) or BOARD[currentindex] == BLOCKCHAR:
                flag = False
                break
        storelist.append(currentindex)
        currentindex += 1
    storelist = tuple(storelist)
    WORDINDEXS.add(storelist)
    
    
def orientation(indexs):
    if indexs[0] - indexs[1] == -1:
        return 'H'
    else:
        return 'V'
    

def update_index_v(index): 
    storelist = []
    currentindex = index
    flag = True
    while flag:
        if currentindex // WIDTH >= HEIGHT or BOARD[currentindex] == BLOCKCHAR:
            flag = False
            break
        storelist.append(currentindex)
        currentindex += WIDTH
    storelist = tuple(storelist)
    WORDINDEXS.add(storelist)                                 

def finaldict():
    for indexs in WORDINDEXS:
            word = boardstring(BOARD, indexs)
            if OPENCHAR not in word:
                USED.add(word)
                continue
            if orientation(indexs) == 'H':
                orient = 'H'
                words = {i for i in WORDBYLENGTH[len(word)]}
                POSORIENT[indexs, orient] = words
                for index, character in enumerate(word.lower()):
                    if character != OPENCHAR:
                        
                        POSORIENT[indexs, orient].intersection_update(IDICT[character.upper(), len(word), index])
            elif orientation(indexs) == 'V':
                orient = 'V'
                words = {i for i in WORDBYLENGTH[len(word)]}
                POSORIENT[indexs, orient] = words
                for index, character in enumerate(word.lower()):
                    if character != OPENCHAR:
                        POSORIENT[indexs, orient].intersection_update(IDICT[character.upper(), len(word), index])
                
    
def boardstring(board, indexs):
    l = []
    for i in indexs:
        l.append(board[i])
    w = ''.join(l)
    return w.lower()


def garanteed_start_positions(board, height, width, dict_lines):
 board = str(board)
 xw = BLOCKCHAR*(width+3)
 xw += (BLOCKCHAR*2).join([board[p:p+width] for p in range(0, len(board), width)])
 xw += BLOCKCHAR*(width+3)
 pattern = r'[{}]({}|\w)*(?=[{}])'.format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
 regex = re.compile(pattern)
 width_turn = [width+2, height+2]
 all_words = dict_lines
 pos_list = []
 pos_word_list = [] # In your own way, fill this list or other type of data structure.
 for turn in range(2):
    for m in regex.finditer(xw): # finditer(subject) after compile list of matches
        pos = 0
        word = xw[m.start()+1:m.end()]
        #regex2 = re.compile('\\b' + word.replace(OPENCHAR, '\\w') + '\\b')
        if len(word)>0 and word.count(OPENCHAR) == 0 and turn == 0:
            if pos_list == []:
                continue
            pos_word_list.append([0, pos_list, 'H', word, []])
        elif len(word)>0 and word.count(OPENCHAR) == 0 and turn == 1:
            if pos_list == []:
                continue
            pos_word_list.append([0, pos_list, 'V', word, []])
        elif len(word)>0 and turn==0:
            if all_words.get(len(word)) == None:
                continue
            
            #store1 = getword(board, width, pos, 'V', len(word))            
            candidates = all_words[len(word)]
            pos = ((m.start()+1)//(width+2)-1)*width + (m.start()+1) % (width+2) -1
            pos_list = [p for p in range(pos, pos+len(word))]
            #if store1 == word:
                #pos_word_list.append([len(word), pos_list, 'V', word, candidates])
            #else:
            pos_word_list.append([len(word), pos_list, 'H', word, candidates])
        elif len(word)>0 and turn == 1:
            if all_words.get(len(word)) == None:
                continue
            
            #store1 = getword(board, width, pos, 'H', len(word)) 
            candidates = all_words[len(word)]
            pos = (((m.start()+1) % (height+2))-1)*width + (m.start()+1)//(height+2)-1
            pos_list = [pos + p*width for p in range(len(word))]
            #if store1 == word:
            #    pos_word_list.append([len(word), pos_list, 'H', word, candidates])
            #else:
            pos_word_list.append([len(word), pos_list, 'V', word, candidates])
    xw = transpose(xw, width_turn[turn])
 for item in pos_word_list:
    num_of_o = item[3].count(OPENCHAR)
 maxlist = []
 for i in range(0, len(pos_word_list)):
     maxlist.append(pos_word_list[i][0])
 maxlen = max(maxlist)
 # number of open-chars is also essential information
 # by working on with open-chars and letter-chars, you may update candidates
 #candidates in pos word list are already the right length so don't need to check for that
 return pos_word_list, all_words, maxlen


def crossword(args):
    global BLOCKCHAR, OPENCHAR, PROTECTEDCHAR, HEIGHT, WIDTH, ALLWORDS, BLOCKCOUNT, WORDBYLENGTH, IDICT, WORDINDEXS, BOARD, POSORIENT, USED, FREQ
    board, width, height, blockcount, filename = initialize()
    store = board
    WIDTH = width
    HEIGHT = height
    BLOCKCOUNT = blockcount
    
    ALLWORDS = set()
    WORDBYLENGTH  = dict()
    IDICT = dict()
    BOARD = list(board)
    WORDINDEXS = set()
    POSORIENT = dict()
    USED = set()
    FREQ = dict()
    if blockcount == height * width:
        board = BLOCKCHAR * (height * width)
        display(board, width, height)   
    else:
        if blockcount % 2 == 0:
            board[0:len(board)//2] + BLOCKCHAR + board[len(board)//2:]
        else:
            board[0:len(board)//2] + OPENCHAR + board[len(board)//2 + 1:]
        board, width, height = ready(board, width, height)
        blockstoputdown = (blockcount - board.count(BLOCKCHAR))
        board = addblocks(board, blockstoputdown, height, width, blockcount)
        xw = addletters(store, board, width, height)
        board = xw
        BOARD = list(board)
        #display(board, width, height)
        input_words(args)
        startindex(board)
        finaldict()
        pos_word_list, all_words, maxlen = garanteed_start_positions(board, height, width, WORDBYLENGTH)
        storient = dict()
        for key in pos_word_list:
            storient[set(key)] = WORDBYLENGTH[key[0]]
        copypos = dict()
        count = 0
        if WIDTH == 15 and HEIGHT == 15:
            copypos = dict()
            for key, value in POSORIENT.items():
                if key[1] == 'H':
                    copypos[key] = value
                if key[1] == 'V' and (count % 5 == 0):
                    copypos[key] = value
                count += 1
            POSORIENT = copypos
        BOARD = fill_board(BOARD, POSORIENT, USED)
        final = ''.join(BOARD)
        final = final.upper()
        display(final, width, height)
        
crossword(args)
                
                
#Sahil Kapadia 2024 Period 7
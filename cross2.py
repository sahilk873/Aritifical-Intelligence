import os, sys, re, random, copy

BLOCKCHAR = '#'
OPENCHAR = '-'
PROTECTEDCHAR = '~'
DICT_LEN = {}
WORD_STRUC = []


def main():
    
    args = ['6x6', 'scrabble.txt', '30']

    inTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.+)$"]
    height, width, blockCt, dictSeen = 4, 4, 0, False
    input_words = []
    for arg in args:
        if os.path.isfile(arg):
            dictLine = open(arg, 'r').read().splitlines()
            sort_by_len(dictLine)  # CREATES SORTED DICTIONARY
            dictSeen = True
            continue
        for testNum, retest in enumerate(inTest):
            match = re.search(retest, arg, re.I)
            if not match: continue
            if testNum == 0:
                height, width = int(match.group(1)), int(match.group(2))
            elif testNum == 1:
                blockCt = int(arg)
            else:
                vpos, hpos, word = int(match.group(2)), int(match.group(3)), match.group(4).upper()
                input_words.append([arg[0].upper(), vpos, hpos, word])  # 2d matrix
    if not dictSeen: exit("bad input")

    #   begin stuff
    size = height * width

    #   first working with 2D matrix
    BOARD = [[OPENCHAR] * width for _ in range(height)]
    if blockCt == size:  # all blocks
        new_b = [[BLOCKCHAR] * width for _ in range(height)]
        # print_board(BOARD)
    elif blockCt == 0:  # no blocks
        new_b = add_words(BOARD, input_words)
        # print_board(BOARD)
    else:  # the likely case
        new_b = do_everything(BOARD, blockCt, height, width, input_words)
        new_b = to_matrix(new_b, width, height)  # turns string in to matrix after blocking
        new_b = add_words(new_b, input_words)

    finished = do_a_weird_thing(new_b, width, height)
    #finished = add_words(finished, input_words)

    print_board(finished)


def do_a_weird_thing(board, w, h):  # only tested with 5x5
    temp_board = board
    dictionary_use = update_hori_poss(board, w)
    used = []

    for p in dictionary_use.keys():
        xpos = p[0]
        ypos = p[1]
        the_word = dictionary_use[p].pop()
        while the_word in used:
            the_word = dictionary_use[p].pop()  # just picks the first word
            the_word = the_word.upper()

        for l in range(0, len(the_word)):
            temp_board[xpos][ypos + l] = the_word[l]
        used.append(the_word)

        """board = temp_board
    board = matrixTranspose(board)
    dictionary_use = update_hori_poss(board, w)

    for p in dictionary_use.keys():
        xpos = p[0]
        ypos = p[1]
        the_word = dictionary_use[p].pop()
        while the_word in used:
            the_word = dictionary_use[p].pop()  # just picks the first word
            the_word = the_word.upper()

        for l in range(0, len(the_word)):
            temp_board[xpos][ypos + l] = the_word[l]
        used.append(the_word)"""

    return temp_board


def add_word(BOARD, word, pos, dir):  # adds to WORD_STRUC, pos is a tuple, ADD TO THIS AFTER PLACING IT
    global WORD_STRUC

    # [word num, position, "word", direction, length, candidates, words affected]
    WORD_NUM = len(WORD_STRUC) + 1
    l = len(word)
    candidates = find_candidates(BOARD, word, pos)
    affect = find_words_affected(BOARD, word, pos)

    new_entry = [WORD_NUM, pos, word, dir, l, candidates, affect]
    WORD_STRUC.append(new_entry)


def remove_word():  # removes from word structure (to remove from board, send back temp
    global WORD_STRUC
    return 0


def find_words_affected(BOARD, word, pos):  # returns set of INDEXES
    affected = set()
    return affected


def update_vert_poss(BOARD):  # THIS IS A MATRIX NOW
    VERT_DICT = {}
    return VERT_DICT


def find_candidates(BOARD, word, position):  # make this better to account for perservation, LOOK BELOW!
    cand = set()
    global DICT_LEN
    cand = find_word_if_there(word, len(word))
    return cand


def find_word_if_there(subs, l):  # substring, length of substring
    global DICT_LEN
    current_list = DICT_LEN[l]
    returnset = set()  # just in case there are more than 1

    num_matches = 0
    test = 0
    for x in subs:
        if x.isalpha():
            num_matches += 1

    for word in current_list:
        temp = word.lower()
        if temp[0] == subs.lower()[0]:  # if the current thing is in thing
            returnset.add(word)
        for i in range(len(word)):
            if subs[i].isalpha() and subs[i] == word[i]:
                test += 1

        if test == num_matches:
            returnset.add(word)

    return returnset  # returns words that can match


def update_hori_poss(BOARD, w):  # THIS IS A MATRIX NOW --> only builds CANDIDATES
    global DICT_LEN
    HORI_DICT = {}  # key is a tuple (x, y) and value is the possible words
    curr_word = []  # list of letters in a word

    for r in range(len(BOARD)):
        i = 1
        for c in range(len(BOARD[r])):
            obj = BOARD[r][c]
            if obj.isalpha() or obj == OPENCHAR or obj == PROTECTEDCHAR:
                if len(curr_word) == 0:  # sets beginngn
                    pos = (r, c)
                curr_word.append(obj)
            if i == w or obj == BLOCKCHAR:  # blockchar
                if len(curr_word) != 0:  # if less than 3, look for words in dict with those first 1 or 2 letters
                    val = len(curr_word)
                    substr = ""
                    wordz_in_dict = []
                    for x in curr_word:
                        if x.isalpha():
                            substr += x
                        else:
                            substr += " "  # placeholder
                    if len(substr) > 0:  # and "&" not in substr:
                        wordz_in_dict = find_word_if_there(substr, val)  # list
                        #if len(wordz_in_dict) == 0:  # this is bad
                            #print("oh you ducked up")
                        if len(wordz_in_dict) != 0:
                            HORI_DICT[pos] = wordz_in_dict
                    else:  # if its really all blank or protected
                        wordz_in_dict = DICT_LEN[val]  # a list
                        HORI_DICT[pos] = wordz_in_dict

                    curr_word = []
            i += 1
    return HORI_DICT

def matrixTranspose(anArray):
    transposed = [None]*len(anArray[0])
    for t in range(len(anArray)):
        transposed[t] = [None]*len(anArray)
        for tt in range(len(anArray[t])):
            transposed[t][tt] = anArray[tt][t]
    return transposed

#   PRELIMINARY BUCKETING (beginning of part 2)
def sort_by_len(dict_list):
    global DICT_LEN
    for l in dict_list:  # l is a string (each word)
        k = len(l)
        if k not in DICT_LEN.keys():
            DICT_LEN[k] = []
            DICT_LEN[k].append(l)
        else:
            DICT_LEN[k].append(l)


def to_matrix(b, w, h):  # goes back to matrix/list of lists
    BOARD = []
    x = 0
    for i in range(h):
        temp_in = []
        for y in range(w):
            temp_in.append(b[x])
            x += 1
        BOARD.append(temp_in)
    return BOARD


def do_everything(BOARD, blockCt, height, width, input_words):
    #   with 2D matrix, it adds words
    BOARD = add_words(BOARD, input_words)  # words, protected and blocks and palindrome and add protect

    #   puts everything to a string
    board = to_string(BOARD)
    board = replace_chars(board)  # changes to protected

    #   recurs to place blocks
    b = ""  # creates copy of the string
    for i in board:
        b += i

    new_board = add_helper(b, blockCt, width, height)  # account for blocks False!

    while not new_board:
        new_board = add_helper(b, blockCt, width, height)  # account for blocks False!

    #   checks connectivity here **
    num_of_blocks = new_board.count(BLOCKCHAR)

    while new_board != False and not check_connectivity(new_board, num_of_blocks, blockCt, height,
                                                        width) or new_board == False or num_of_blocks != blockCt:  # fix x and num
        new_board = add_helper(new_board, blockCt, width, height)
        new_board = symmetrize(new_board)

        new_board = fix_board(width, new_board, height)

    return new_board


def remove_border(xw, w, h):
    b = xw[w + 3:len(xw) - w - 1]
    m = 0
    board = ""
    for i in range(h):
        board += b[m:m + w]
        m += w + 2
    return board


def print_board(b):  # prints board for MATRIX
    for x in b:
        for y in x:
            print(y, end=" ")
        print()


def display(w, h, b):  # prints the board
    i = 0
    s = w * h  # size

    while i < s:
        for x in range(h):
            for y in range(w):
                print(b[i], end=" ")
                i += 1
            print()


def to_string(b):  # turns matrix in to string
    return ''.join(str(item) for b[0] in b for item in b[0])


def symmetrize(xw):  # symmetrizes everything
    if xw == False: return False
    for i in range(len(xw)):
        if xw[len(xw) - i - 1] == OPENCHAR and xw[i] != OPENCHAR:
            xw = xw[:len(xw) - i - 1] + xw[i] + xw[len(xw) - i:]
    return xw


def add_words(b, a):  # adds the words, using a 2D matrix for ease
    new_board = b

    for word in a:  # list in the big list
        d = word[0]  # H or V
        xpos = word[1]
        ypos = word[2]
        the_word = word[3]  # word

        if (d == 'H'):  # horizontal words
            for l in range(0, len(the_word)):
                new_board[xpos][ypos + l] = the_word[l]
        elif (d == 'V'):  # vertical words
            for m in range(0, len(the_word)):
                new_board[xpos + m][ypos] = the_word[m]

    return new_board


def update_pos_list(b):  # list of open chars
    pos_list = []
    for x in range(len(b)):
        if (b[x] == OPENCHAR and b[len(b) - x - 1] == OPENCHAR): pos_list.append(x)
    return pos_list


def transpose(b, w):  # tranposes elements in string
    return "".join([b[col::w] for col in range(w)])


def replace_chars(xword):  # protects
    c = 0
    while c < len(xword):
        curr = xword[c]
        if curr != OPENCHAR and curr != PROTECTEDCHAR:
            xword = xword.replace(xword[c], PROTECTEDCHAR)
        c += 1
    return xword


def fix_board(width, xword, height):  # code given
    #   adds border here
    if xword == False: return False

    xw = BLOCKCHAR * (width + 3)
    xw += (BLOCKCHAR * 2).join([xword[p:p + width] for p in range(0, len(xword), width)])
    xw += BLOCKCHAR * (width + 3)

    illegalRegex = "[{}](.?[{}]|[{}].?)[{}]".format(BLOCKCHAR, PROTECTEDCHAR, PROTECTEDCHAR, BLOCKCHAR)
    il2 = "[{}](.?[{}]|[{}].?)[{}]".format(BLOCKCHAR, OPENCHAR, PROTECTEDCHAR, BLOCKCHAR)
    substituteRegex = "[{}]{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)  # #-#
    subRE2 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)  # #--#
    subRE3 = "[{}]{}{}{}[{}]".format(BLOCKCHAR, OPENCHAR, PROTECTEDCHAR, PROTECTEDCHAR, BLOCKCHAR)  # #-~~#

    newH = len(xw) // (width + 2)
    for counter in range(2):
        xw = re.sub(substituteRegex, BLOCKCHAR * 2, xw)
        xw = re.sub(subRE2, BLOCKCHAR * 3, xw)
        xw = re.sub(subRE3, BLOCKCHAR + PROTECTEDCHAR * 3, xw)
        if re.search(illegalRegex, xw) or re.search(il2, xw): return False  # here are problems

        xw = transpose(xw, len(xw) // newH)
        newH = len(xw) // newH

    if re.search(illegalRegex, xw) or re.search(il2, xw): return False  # here are problems

    new_board = remove_border(xw, width, height)
    new_board = symmetrize(new_board)

    return new_board


def add_helper(b, count, width, height):
    # updates
    b = symmetrize(b)
    b = fix_board(width, b, height)

    if b == False:  # checks if false before proceeded
        return False
    if count == b.count(BLOCKCHAR):  # base case
        return b
    elif b.count(BLOCKCHAR) > count:
        return False

    plist = update_pos_list(b)  # pos list or open spots!

    position = random.choice(plist)  # picks random
    temp = b[:position] + BLOCKCHAR + b[position + 1:]  # adds in block
    # recurs
    result = add_helper(temp, count, width, height)

    if result != False:
        # updates
        result = symmetrize(result)
        result = fix_board(width, result, height)

        # recurs
        return result
    # if all fails...
    return False


def check_connectivity(board, x, num, height, width):
    if x > num or board.count(OPENCHAR) == 0: return True

    count, start_pos = 0, 0

    while start_pos < len(board) and board[start_pos] == BLOCKCHAR: start_pos += 1
    dirs = [-1, width, 1, -1 * width]

    temp_board = area_fill(board, start_pos, dirs, width)
    count = temp_board.count('?')
    count2 = board.count(OPENCHAR) + board.count(PROTECTEDCHAR)

    return count == count2


def area_fill(board, sp, dirs, width):
    if sp < 0 or sp >= len(board): return board
    if board[sp] in {OPENCHAR, PROTECTEDCHAR}:
        board = board[0:sp] + '?' + board[sp + 1:]
        for d in dirs:
            if d == -1 and sp % width == 0: continue  # left edge
            if d == 1 and sp + 1 % width == 0: continue  # right edge
            board = area_fill(board, sp + d, dirs, width)
    return board


# main method
main()
# python working2.py 9x13 19 wordsC.txt V0x1Dog
# python working2.py 4x4 0 wordsC.txt
# python working2.py wordsC.txt 5x5 4 "v4x3S"
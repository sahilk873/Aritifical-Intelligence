import sys; args = sys.argv[1:]
idx = int(args[0])-40
myRegexLst = [
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//"] #starts with one or two, or is just zero

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Sahil 2024 7



import sys; args = sys.argv[1:]
idx = int(args[0])-50
myRegexLst = [
    r"/(\w)+\w*\1\w*/i",
    r"/(\w)*(\w*\1){3}\w*/i",
    r"/^(1[10]*1|0[10]*0|0|1)$/",
    r"/\b(?=\w*cat)\w{6}\b/i",
    r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
    r"/\b(?!\w*cat)\w{6}\b/i",
    r"/\b(?!\w*(\w)\w*\1)\w*[^!. ]/i",
    r"/^(?!.*10011)[01]*$/",
    r"/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i",
    r"/^(?!.*1.1)[01]*$/"] #starts with one or two, or is just zero

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Sahil 2024 7
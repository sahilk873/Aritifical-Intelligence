# Nicole Kim, 2/9/2019, edited on 2/1/2021
import re
import sys; args = sys.argv[1:]

def num_30(str):
   # Current test checks if the string is '0' 
   pattern = "^10[01]|0$"   #notice that python does not want / /
   match = re.match(pattern, str)
   print ("string is either 0, 100, or 101: ", match != None)

def num_31(str):
   # Current test checks if the string is '0' 
   pattern = "^[01]*$"
   print ("string is a binary string:", re.match(pattern, str) != None)

# Pre-condition: input is a binary string, so you do not need to check if it's a binary or not.
def num_32(str):
   pattern = '/d*[0, 2, 4, 6, 8]'
   print ("string is an even binary number:", re.match(pattern, str) != None)

def num_33(str):
   # Current test searches words with 'a' 
   pattern = "\w.*[aeiou]\w.*[aeiou].*"
   # Notice that python does not support /i in the pattern. 
   # Use re.I for case insensitive when you match(exact same) or search(has one or more)
   print ("there's a word at least two vowels:", re.search(pattern, str, re.I) != None)

def num_34(str):
   pattern = "^\d{3} *-? *\d\d *-? *\d{4}$"
   print ("even binary integer string:", re.match(pattern, str) != None)

def num_35(str):
   pattern = "^[01]*110[01]*$"
   print ("binary string including 110:", re.match(pattern, str) != None)

def num_36(str):
   pattern = "^.{2,4)$"
   print ("length at least two, but at most four:", re.match(pattern, str, re.DOTALL) != None)

def num_37(str):
   pattern = "^\d{3} *-? *\d\d *-? *\d{4}$"
   print ("valid social security number:", re.match(pattern, str) != None)

def num_38(str):
   # When you read multiline input such as "I\nAM\nSAM."
   # str = str.replace('\\n', '\n') # If you need this...
   pattern = ""
   
   # When you want to use /im options:
   d_search = re.search(pattern, str, re.I | re.MULTILINE)
   print ("first word with d on a line:", d_search != None)

def num_39(str):
   pattern = ""
   print ("There's same number of 01 substrings as 10 substrings: ", re.match(pattern, str) != None)

while(True):
   input_num = input("Choose the exercise # (30 - 39 or -1 to terminate):")
   if input_num == '-1': exit("Good bye")
   input_str = input("Input string: ")
   eval("num_"+input_num)(input_str)
   print()
   
import sys; args = sys.argv[1:]

idx = int(args[0])-30 # 30-39
myRegexList = [
"/^0$|^10[01]$/",
"/^[01]*$/",
"/0$/",
"/\w*[aeiou]\w*[aeiou]\w*/i",
"/^0$|^1[01]*0$/",
"/^[01]*110[01]*$/",
"/^.{2,4}$/s",
"/^\d{3} *-? *\d\d *-? *\d{4}$/",
"/^.*?d\w*/mi",
"/^0[01]*0$|^1[01]*1$/",
""
]
print(myRegexList[idx])

#Sahil Kapadia 2024 Period 7

   
''' Sample Output
Choose the exercise # (30 - 39 or -1 to terminate):30
Input string: 100
string is either 0, 100, or 101:  True

Choose the exercise # (30 - 39 or -1 to terminate):30
Input string: 1000
string is either 0, 100, or 101:  False

Choose the exercise # (30 - 39 or -1 to terminate):39
Input string: 101
There's same number of 01 substrings as 10 substrings:  True

Choose the exercise # (30 - 39 or -1 to terminate):39
Input string: 100
There's same number of 01 substrings as 10 substrings:  False

Choose the exercise # (30 - 39 or -1 to terminate):39
Input string: 0
There's same number of 01 substrings as 10 substrings:  True

Choose the exercise # (31 - 40 or -1 to terminate):-1
Good bye

 ----jGRASP wedge2: exit code for process is 1.
 ----jGRASP: operation complete.

'''
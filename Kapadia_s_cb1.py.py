#Sahil Kapadia 


def sleep_in(weekday, vacation):
  return not(weekday) or vacation

def monkey_trouble(a_smile, b_smile):
  return (a_smile == b_smile)

def sum_double(a, b):
  return (2 *( a+ b)) if a==b else a + b

def diff21(n):
  return 2*(n-21) if n> 21 else abs(n-21)

def parrot_trouble(talking, hour):
  return (talking and (hour < 7 or hour > 20))

def makes10(a, b):
  return (a == 10) or (b == 10) or (a + b == 10)

def near_hundred(n):
  return (abs(n-100) <= 10) or (abs(n-200) <= 10)

def pos_neg(a, b, negative):
  return (negative and (a < 0 and b < 0)) or (not negative and ((a > 0 and b < 0) or (a < 0 and b > 0)))

def hello_name(name):
  return "Hello " + name + "!"

def make_abba(a, b):
  return a + b + b + a

def make_tags(tag, word):
  return "<" + tag + ">" + word + "</" + tag + ">"

def make_out_word(out, word):
  return out[:2] + word + out[2:]

def extra_end(str):
  return str[-2:]*3

def first_two(str):
  return str[:2]

def first_half(str):
  return str[:len(str)//2]

def without_end(str):
  return str[1:len(str)-1]

def first_last6(nums):
  return (nums[0] == 6) or (nums[len(nums)-1] == 6) 



def make_pi(n)
    return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7][:n]

def common_end(a, b):
  return (a[0] == b[0] or a[-1] == b[-1])

def sum3(nums):
  return sum[nums]

def rotate_left3(nums):
  return [nums[1], nums[2], nums[0]]

def reverse3(nums):
  return nums[::-1]

def max_end3(nums):
  return [nums[0]] * 3 if nums[0] >= nums[-1] else [nums[-1]] * 3

def sum2(nums):
  return 0 if len(nums) = 0 else nums[0] + nums[1]

def cigar_party(cigars, is_weekend):
  return (is_weekend and cigars >= 40) or (cigars >= 40 and cigars <=60)

def date_fashion(you, date):
  return 0 if (date <= 2 or you <= 2) else 2 if (you >= 8 or date >= 8) else 1
  
def squirrel_play(temp, is_summer):
    return temp in range(60, 91 if not(is_summer) else 101)

def caught_speeding(speed, is_birthday):
  return 0 if speed <= 60 + int(is_birthday)*5 else 1 if speed<= 80 + int(is_birthday)*5 else 2

def sorta_sum(a, b):
  return a+b if a+b not in range (10, 20) else  20

def alarm_clock(day, vacation):
  return "7:00" if (day in range(1, 6) and not vacation) else "off" if (day not in range(1, 6) and vacation) else "10:00" 

def love6(a, b):
  return a == 6 or b == 6 or a+b == 6 or abs(a-b) ==6 

def in1to10(n, outside_mode):
  return (not outside_mode and (n in range(1, 11))) or (outside_mode and (n <= 1 or n>= 10))

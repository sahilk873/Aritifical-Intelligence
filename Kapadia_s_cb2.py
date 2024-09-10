#3.57
def string_times(str, n):   
  return str*n

#3.57
def front_times(str, n):  
  return str[:3]*n

#3.57
def string_bits(str):       
  return str[::2]

#3.46
def string_splosion(str):   
  return "".join(str[:n] for n in range(len(str)+1))

#3.39
def last2(str):                         
  return  sum(str[i:i+2] == str[-2:] for i in range(len(str)-2))

#3.57
def array_count9(nums):   
  return nums.count(9)

#3.57
def array_front9(nums):     
  return 9 in nums[:4]

#3.55
def array123(nums):        
  return (1, 2, 3) in zip(nums, nums[1:], nums[2:])
  
#3.49
def string_match(a, b):     
  return sum(a[i:i+2]==b[i:i+2] for i in range(len(a)-1))

#3.54
def double_char(str):       
  return "".join(x+x for x in str)

#3.57
def count_hi(str):         
  return str.count("hi")

#3.53
def cat_dog(str):        
  return str.count("cat") == str.count("dog")

#3.45
def count_code(str):        
  return list(zip(str, str[1:], str[3:])).count(('c', 'o', 'e'))

#3.35
def end_other(a, b):
  return b.lower().endswith(a.lower()) or a.lower().endswith(b.lower())

#3.57
def xyz_there(str):         
  return "xyz" in str.replace(".x", "q")

#3.57
def make_bricks(small, big, goal):
  return goal-big*5<=small>=goal%5

#3.38
def lone_sum(a, b, c):       
  return sum(x for x in (a, b, c) if (a, b, c).count(x) == 1)

#3.52
def lucky_sum(a, b, c):       
  return sum([a, b, c][:[a, b, c, 13].index(13)])

#3.48
def no_teen_sum(a, b, c):     
  return sum(x for x in (a, b, c) if (x < 13 or x >19) or x in (15, 16))

#3.45
def round_sum(a, b, c):       
  return int(sum(round(x+.1, -1) for x in (a, b, c)))

#3.57
def close_far(a, b, c):      
  return (abs(a-b) > 1) ^ (abs(a-c) > 1) and abs(b-c) > 1 

#3.55
def make_chocolate(small, big, goal): 
  return [x:= goal-min(big, goal//5)*5, -1][x>small]

#3.57
def count_evens(nums):
  return sum(~n%2 for n in nums)

#3.57
def big_diff(nums):
  return max(nums)-min(nums)

#3.53
def centered_average(nums):
  return (sum(nums) - max(nums) - min(nums))// (len(nums)-2)

#3.16
def sum13(nums):                
  return sum(x for i, x in enumerate(nums) if x != 13 and (i == 0 or nums[i-1] != 13))

#3.57
def has22(nums):             
  return (2, 2) in zip(nums, nums[1:])

#3
def sum67(nums):
  return sum(nums) if (6 not in nums) else sum(nums[:nums.index(6)]) + sum67(nums[nums.index(7, nums.index(6)+1)+1:])

#Sahil Kapadia 2024 7 Kim
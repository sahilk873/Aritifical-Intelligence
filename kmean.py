''' Test cases:
6 https://cf.geekdo-images.com/imagepage/img/5lvEWGGTqWDFmJq_MaZvVD3sPuM=/fit-in/900x600/filters:no_upscale()/pic260745.jpg
10 cute_dog.jpg
6 turtle.jpg
'''
import PIL
from PIL import Image
import urllib.request
import io, sys, os, random
import tkinter as tk
from PIL import Image, ImageTk  # Place this at the end (to avoid any conflicts/errors)



def choose_random_means(k, img, pix):
    
    width, height = img.size[0], img.size[1]
    random_pixels = []
    for i in range(k):
        random_x = int(random.uniform(0, width-1))
        random_y = int(random.uniform(0, height-1))
        pixel = pix[random_x, random_y]
        random_pixels.append(pixel)

    return random_pixels


# goal test: no hopping
def check_move_count(mc):
   for move in mc:
      if move != 0:
         return False
   return True

# calculate distance with the current color with each mean
# return the index of means
def dist(col, means):
   minIndex, dist_sum = 0, 255**2+255**2+255**2
   for i in range(len(means)):
        sum = 0
        for j in range(len(col)):
             sum += (col[j]-means[i][j])**2
        sum = sum**0.5
        if sum < dist_sum:
             minIndex = i
             dist_sum = sum
   return minIndex

def clustering(p, img, pix, cb, mc, means, count):
    temp_pb, temp_mc, temp_m = [[] for x in means], [], []
    temp_cb = [0 for x in range(len(means))]
    for tup in p:
        min_dist = float('inf')
        min_idx = -1
        for k in range(len(means)):
            dist = abs(tup[0] - means[k][0]) + abs(tup[1] - means[k][1]) + abs(tup[2] - means[k][2])
            if dist < min_dist:
                min_dist = dist
                min_idx = k
        temp_cb[min_idx] += 1
        temp_pb[min_idx].append(tup)
    temp_mc = [a - b for a, b in zip(temp_cb, cb)]
    m = []
    for li in temp_pb:
        sum_r, sum_g, sum_b = 0, 0, 0
        for tup in li:
            sum_r += tup[0]
            sum_g += tup[1]
            sum_b += tup[2]
        temp_m.append(((sum_r / len(li)), (sum_g / len(li)), (sum_b / len(li))))
        if check_move_count(temp_mc):
            m = []
            m.append((sum_r/len(li), sum_g / len(li), sum_b/len(li)))
    print('diff', count, ':', temp_mc)
    return temp_cb, temp_mc, temp_m, m

def update_picture(img, pix, means):
    region_dict = {}
    tup = []
    width, height = img.size[0], img.size[1]
    for i in range(width):
        for j in range(height):
            pixel = pix[i, j]
            tup = (pixel[0], pixel[1], pixel[2])
            min_dist = float('inf')
            min_idx = -1
            for k in range(len(means)):
                dist = abs(tup[0] - means[k][0]) + abs(tup[1] - means[k][1]) + abs(tup[2] - means[k][2])
                if dist < min_dist:
                    min_dist = dist
                    min_idx = k
            r, g, b = means[min_idx]
            r, g, b = int(r), int(g), int(b)
            pix[i, j] = (r, g, b)
            if min_idx in region_dict:
                region_dict[min_idx].append((i, j))
            else:
                region_dict[min_idx] = [(i, j)]

    return pix, region_dict

def distinct_pix_count(img, pix):
   cols = {}
   max_col, max_count = pix[0, 0], 0
   return len(cols.keys()), max_col, max_count

def count_regions(img, region_dict, pix, means):
   region_count = [0 for x in means]
   return region_count

 
def main():
   #k = int(sys.argv[1])
   #file = sys.argv[2]
   k = 10
   file = 'cute_dog.jpg'
   if not os.path.isfile(file):
      file = io.BytesIO(urllib.request.urlopen(file).read())
   
   window = tk.Tk() #create an window object
   
   img = Image.open(file)
   
   img_tk = ImageTk.PhotoImage(img)
   lbl = tk.Label(window, image = img_tk).pack()  # display the image at window
   
   pix = img.load()   # pix[0, 0] : (r, g, b) 
   print ('Size:', img.size[0], 'x', img.size[1])
   print ('Pixels:', img.size[0]*img.size[1])
   d_count, m_col, m_count = distinct_pix_count(img, pix)
   print ('Distinct pixel count:', d_count)
   print ('Most common pixel:', m_col, '=>', m_count)

   count_buckets = [0 for x in range(k)]
   move_count = [10 for x in range(k)]
   means = choose_random_means(k, img, pix)
   print ('random means:', means)
   count = 1
   p = []
   width, height = img.size[0], img.size[1]
   for i in range(width):
        for j in range(height):
            pixel = pix[i, j]
            p.append(pixel)
   while not check_move_count(move_count):
      count += 1
      count_buckets, move_count, means, m = clustering(p, img, pix, count_buckets, move_count, means, count)
      if count == 2:
         print ('first means:', means)
         print ('starting sizes:', count_buckets)
   pix, region_dict = update_picture(img, pix, means)  # region_dict can be an empty dictionary
   print ('Final sizes:', count_buckets)
   print ('Final means:')
   for i in range(len(means)):
      print (i+1, ':', means[i], '=>', count_buckets[i])
      
   img_tk = ImageTk.PhotoImage(img)
   lbl = tk.Label(window, image = img_tk).pack()  # display the image at window
   
   img.save('output1.png', 'PNG')  # change to your own filename
   window.mainloop()
   #img.show()
   
if __name__ == '__main__': 
   main()
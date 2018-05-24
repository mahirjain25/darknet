'''
Function that writes the annotation files for each image, as per the YOLOV2 format, which will be used by the
 Darknet config (.cfg) file.
 
Parameters/Variables:
oldpath - Path of file to be annotated.
newpath - Path of modified annotated file.
imagepath - Path of image that is getting annotated
width - Width of entire image, not bounding box. 
height - Height of entire image, not bounding box.
xmin - Smallest x co-ordinate of bounding box (Left x value)
xmax - Largest x co-ordinate of bounding box (Right x value)
ymin - Smallest y co-ordinate of bounding box
ymax - Largest y co-ordinate of bounding box
l - Class label of character in the bounding box
'''
from PIL import Image

def write_annotation(imagepath,oldpath,newpath):
	file_read = open(oldpath,'r')
	file_write = open(newpath,'w')
	lines = file_read.read().split("\n") #for ubuntu, use "\r\n" instead of "\n"
	print (lines)
	# for line in lines:
	# 	print (len(line))
	# 	elems = line.split(' ')
	# 	print (elems)
	# 	e = elems.split('\n')
	# 	print(int(e[0]),int(e[1]))
	for line in lines:
		if(len(line) >= 3):
			elems = line.split(" ")
			print(elems)
			xmin = int(elems[0])
			xmax = int(elems[2])
			ymin = int(elems[1])
			ymax = int(elems[3])
			im=Image.open(imagepath)
			width= int(im.size[0])
			height= int(im.size[1])
			dw = 1./width
			dh = 1./height
			x = (xmin+xmax)/2.0
			y = (ymin+ymax)/2.0
			w = xmax - xmin
			h = ymax - ymin
			x = x * dw
			y = y * dh
			w = w * dw
			h = h * dh 
			file_write.write(str(x)+" "+str(y)+" "+str(w)+" "+str(h)+"\n")
		elif len(line) == 2:
			print(line)
			file_write.write(line+" ")


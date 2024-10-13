# based off https://www.morethantechnical.com/blog/2020/03/21/packing-better-montages-than-imagemagick-with-python-rect-packer/

import cv2
import os
import glob
from rectpack import newPacker
import rectpack #https://github.com/secnot/rectpack
import pickle
import numpy as np
import argparse



IMAGE_FOLDER = r"C:\Users\andre\Desktop\mothbox_dataset_3000_2024-10-10\images\train\x-anylabeling-matting"
#BACKGROUND_COLOR = (28, 242, 167) #nice pastel green
BACKGROUND_COLOR = (242, 168, 28) #nice pastel orange
#BACKGROUND_COLOR = (211, 28, 242) #nice pastel fucsia
#BACKGROUND_COLOR =(230, 242, 28) #nice pastel yellow
#BACKGROUND_COLOR =(242, 43, 29) #nice pastel red
#BACKGROUND_COLOR =(29, 241, 242) #nice pastel blue
#BACKGROUND_COLOR =(179, 242, 29) #nice yellow green
#BACKGROUND_COLOR =(242, 29, 139) #hot pink
ASPECT_RATIO=0.707  #A4 paper ratio 1.414 in portrait or  0.707 in landscape   # Letter paper is 215.9 x 279.4mm 1.29:1 ratio or 0.775 landscape
# Mothbox board is about 4370 pixels wide and 290mm wide. Which means we tend to shoot images that are 15px per mm
#BACKGROUND_COLOR= (0,0,0) #black
BACKGROUND_ALPHA=255
PIX_PER_MM=15

# An A4 sheet is 210mm W x 297mm H, so an output width for a A4 sheet would be 210mm x 15px/mm = 3150 for realistic insect sizes if printed full portrait mode
# Or 297x15 = 4455 for landscape mode
#  a letter sized sheet is 279.4x15 or 4191pixels wide (landscape)

OUTPUT_WIDTH=4191


IMAGE_SCALE_PERCENT=100
SORT_ALGO = 1
MIN_IMAGE_DIM=4 #minimum width of an image to work with
MAX_NUM_PAGES =100  # Replace with your desired max number of bins

# This is a handy function that crops images edges if they are all black or alpha to get to the core of the image
def crop(image):
    th =30 
    y_nonzero, x_nonzero, _ = np.nonzero(image>th)
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]

def makeImage(binnum,output_im,background_image):
    output_im=background_image
    print('used %d of %d images' % (len(used), len(files)))

    sub_output_path = IMAGE_FOLDER+"/visualizations"
    if not os.path.exists(sub_output_path):
        os.makedirs(sub_output_path)

    print('writing image output '+sub_output_path+"/output_"+str(IMAGE_SCALE_PERCENT)+ "percent_"+str(SORT_ALGO)+"sort"+str(binnum)+".png")



    cv2.imwrite(sub_output_path+"/output_"+str(IMAGE_SCALE_PERCENT)+ "percent_"+str(SORT_ALGO)+"sort_"+str(binnum)+".png", output_im)



parser = argparse.ArgumentParser(description='Montage creator with rectpack')
parser.add_argument('--width', help='Output image width', default=OUTPUT_WIDTH, type=int)
parser.add_argument('--aspect', help='Output image aspect ratio, \
    e.g. height = <width> * <aspect>', default=ASPECT_RATIO, type=float)
parser.add_argument('--output', help='Output image name', default=IMAGE_FOLDER+'/0_output.png')
parser.add_argument('--input_dir', help='Input directory with images', default=IMAGE_FOLDER)
parser.add_argument('--debug', help='Draw "debug" info', default=False, type=bool)
parser.add_argument('--border', help='Border around images in px', default=0, type=int)
args = parser.parse_args()



files = sum([glob.glob(os.path.join(args.input_dir, '*.' + e)) for e in ['jpg', 'jpeg', 'png']], [])
print('found %d files in %s' % (len(files), args.input_dir))
print('getting images sizes...')

sizes=[]
for image_path in files:

    f = open(image_path, "rb")  # have to do this silly stuff where we open it because imread cannot read paths with accents!
    buff = f.read()
    f.close()

    buff = np.frombuffer(buff, dtype=np.uint8)
    image = cv2.imdecode(buff, cv2.IMREAD_UNCHANGED)

    image=crop(image)
    if(image.shape[0]<MIN_IMAGE_DIM or image.shape[1]<MIN_IMAGE_DIM): #there can be an error where an entire image gets cropped away, need to add a catch that throws away too tiny images
        continue
    #optionally scale the images
    if(IMAGE_SCALE_PERCENT!=100):
        width = int(image.shape[1] * IMAGE_SCALE_PERCENT / 100)
        height = int(image.shape[0] * IMAGE_SCALE_PERCENT / 100)
        dim = (width, height)
        
        if(width<MIN_IMAGE_DIM or height<MIN_IMAGE_DIM): #there can be an error where an entire image gets cropped away, need to add a catch that throws away too tiny images
            continue
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


    filename_and_shape=[image_path,image.shape]
    sizes.append(filename_and_shape)
#sizes = [(im_file, cv2.imread(im_file).shape) for im_file in files]


# Prepare the Packer
#----------------------------

# NOTE: you could pick a different packing algo by setting pack_algo=..., e.g. pack_algo=rectpack.SkylineBlWm

#packer = newPacker(rotation=True, pack_algo=rectpack.GuillotineBssfSas)#Cannot currently do rotation because it confuses the algo and switches their locations)

if(SORT_ALGO==0):
    sortalgorithm=rectpack.SORT_NONE
elif(SORT_ALGO==1):
    sortalgorithm=rectpack.SORT_AREA
elif(SORT_ALGO==2):
    sortalgorithm=rectpack.SORT_PERI
elif(SORT_ALGO==3):
    sortalgorithm=rectpack.SORT_SSIDE
elif(SORT_ALGO==4):
    sortalgorithm=rectpack.SORT_LSIDE
elif(SORT_ALGO==5):
    sortalgorithm=rectpack.SORT_RATIO



packer = newPacker(rotation=False, sort_algo=sortalgorithm) 
#print(sizes)

print("adding rects")
for i, r in enumerate(sizes):
    #print(i)
    #print(r[1])

    packer.add_rect(r[1][1] + args.border * 2, r[1][0] + args.border * 2, rid=i)
out_w = args.width
aspect_ratio_wh = args.aspect
out_h = int(out_w * aspect_ratio_wh)

nbins = MAX_NUM_PAGES  

for i in range(nbins):
    packer.add_bin(out_w, out_h)


#~~~~~~~~~~~~~~ PACKING ~~~~~~~~~~~~~~~~~~~~~~~~~
print('packing...')
packer.pack()


output_im = np.full((out_h, out_w, 4), 255, np.uint8)

rgb_color=BACKGROUND_COLOR
# Since OpenCV uses BGR, convert the color first
color = tuple(reversed(rgb_color))
# Fill image with color
background_image = np.full((out_h, out_w, 4), 0, np.uint8) # fill a full BGRA background image black transparency
BGRAcolor= color+ (BACKGROUND_ALPHA,)
background_image[:] = BGRAcolor

used = []

nbins=len(packer)
print("bins ",nbins)


bin=0

for rect in packer.rect_list():

    b, x, y, w, h, rid = rect



    if(bin!=b):
        #save previous image
        makeImage(bin,output_im,background_image)
        #reset background
        background_image = np.full((out_h, out_w, 4), 0, np.uint8)
        background_image[:] = BGRAcolor
        bin=b
    used += [rid]
    orig_file_name = sizes[rid][0]


    #cant just use imread with files with accents
    #im = cv2.imread(orig_file_name, cv2.IMREAD_COLOR)
    f = open(orig_file_name, "rb")  # have to do this silly stuff where we open it because imread cannot read paths with accents!
    buff = f.read()
    f.close()

    buff = np.frombuffer(buff, dtype=np.uint8)
    im = cv2.imdecode(buff, cv2.IMREAD_UNCHANGED)
    im=crop(im)

    #optionally scale the images
    if(IMAGE_SCALE_PERCENT!=100):
        width = int(im.shape[1] * IMAGE_SCALE_PERCENT / 100)
        height = int(im.shape[0] * IMAGE_SCALE_PERCENT / 100)
        dim = (width, height)
        im = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)


    overlay_color=im[:, :, :4]
    overlay_alpha = im[:, :, 3]
    # Create masks and inverse masks using the alpha channel
    mask = overlay_alpha / 255.0
    inv_mask = 1.0 - mask

    #output_im[out_h - y - h + args.border : out_h - y - args.border, x + args.border:x+w - args.border] = im

    # Get the region of interest (ROI) from the background
    roi = background_image[out_h - y - h + args.border : out_h - y - args.border, x + args.border:x+w - args.border]


    # Blend the overlay with the ROI
    for c in range(0, 4):
        roi[:, :, c] = (overlay_color[:, :, c] * mask + roi[:, :, c] * inv_mask)

    background_image[out_h - y - h + args.border : out_h - y - args.border, x + args.border:x+w - args.border] = roi


    
    
    if args.debug:
        cv2.rectangle(output_im, (x,out_h - y - h), (x+w,out_h - y), (255,0,0), 3)
        cv2.putText(output_im, "%d"%rid, (x, out_h - y), cv2.FONT_HERSHEY_PLAIN, 3.0, (0,0,255), 2)

#gotta do one last one to catch the final ones
makeImage(bin,output_im,background_image)


print('done.')
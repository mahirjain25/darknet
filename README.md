![Darknet Logo](http://pjreddie.com/media/files/darknet-black-small.png)

# Darknet #
Darknet is an open source neural network framework written in C and CUDA. It is fast, easy to install, and supports CPU and GPU computation.

For more information see the [Darknet project website](http://pjreddie.com/darknet).

For questions or issues please use the [Google Group](https://groups.google.com/forum/#!forum/darknet).



# Using Darknet for Custom Object Detection with YOLOv2

- Clone Darknet
`git clone https://github.com/pjreddie/darknet.git`
- Open the Makefile, and configure as per your system setup. 
``cd darknet``  
``vi Makefile``  

Then Accordingly set flags to 1, as per system specifications: (If system is confifured for the flags)  
```  
GPU=0          
CUDNN=0    
OPENCV=0
OPENMP=0
DEBUG=0
```  
Now run:  
`make`  

#### Now, darknet is ready to use. Note: Any time changes are made to the setup, make needs to be executed. This includes changes to scripts under src/, as well as the makefile.

Verify installation with :  
`./darknet`  
`output: usage: ./darknet <function>`  


## Training

Create a directory called train with the following path, relative to darknet/ :  
`data/train`

Place all training images in this folder (.jpg format)  
Now, annotations for these images need to be placed in the same folder, one annotation file per image (.txt format)

Example of directory structure:
Contents of `data/train`:  
im0.jpg  
im0.txt  
im1.jpg  
im1.txt
...
and so on.

###### A small note about Annotations

Annotations are needed to specify what class label is present in the box, as well as specify the coordinates of the box.

Typically, one uses BBoxLabel tool to annotate the images. [See Here](https://github.com/puzzledqs/BBox-Label-Tool)
The Annotations created by this are of the format:  
_Class-Label_  
_box-left-x box-top-y box-right-x box-bottom-y_

This needs to be converted into a format specific to darknet:  
_Class-Label object-center-in-x object-center-in-y object-width-in-x object-width-in-y_   

This can be done using the script from [here.](https://github.com/mahirjain25/darknet/blob/master/scripts/convert_annotations.py)  

Note: The class labels for annotations in the .txt files must be integers, not strings.  
The integers can be mapped to strings in obj.names, as described in the next sub-section.  


**Continue only if data/train/ has been populated with all images and their annotations as per the darknet format.**



#### Setting up the configuration files

- Create obj.names under /data and write the names of the classes (these will map to the integer class labels in the annotation files). It is important to keep note of which class corresponds to which integer value.  

- Create obj.data under /data, and in it add (change classes as per the number of classes you have):  
classes= 1  
train  = data/train.txt  
valid  = data/test.txt  
names = data/obj.names  
backup = backup/  

- Create a file data/train.txt , that has the absolute paths to each training image, on a new line. Example:  

`/home/mahir/darknet/data/train/im0.jpg  `
`/home/mahir/darknet/data/train/im1.jpg  `
`/home/mahir/darknet/data/train/im2.jpg  `

Now, we must choose an appropriate network for learning the weights. The most common strategy employed for Custom Object Detection is:
Create file yolo-obj.cfg with the same content as in yolo-voc.2.0.cfg (or copy yolo-voc.2.0.cfg to yolo-obj.cfg) and:
- change line batch to batch=64 (comment out batch = 1)
- change line subdivisions to subdivisions=8 (comment out subdivisions = 1)
- change line #244, classes=20 to your number of objects
- change line #237, from filters=125 to: filters=(classes + 5)x5, so if classes=2 then it should be filter=35. 
- change line #20, max_batches = The number of epochs you wish to carry out training.

The above model is highly recommended. One may experiment with the multiple models available in cfg/. 
Place yolo-obj.cfg in the main (darknet/) directory. 

#### Starting the training process

**Note - Re-check your configuration files mentioned in the last step before proceeding.**

Download pre-trained weights from [here](https://pjreddie.com/media/files/darknet19_448.conv.23)  
Place the downloaded file in darknet/.  

Open a terminal, navigate to darknet/ and then use the command: 
`./darknet detector train data/obj.data yolo-obj.cfg darknet19_448.conv.23`

This will begin training. There are a couple of really good resources on what the output means, and when to stop training.  
Check these links to understand:  
[Link 1](https://timebutt.github.io/static/understanding-yolov2-training-output/)  
[Link 2](https://github.com/pengdada/darknet-win-linux#when-should-i-stop-training) 

One can interrupt training using `Control+C`. The weights save in the backup/ folder after intervals of 100 epochs.

**Note  - One can resume from a checkpoint using ./darknet detector train data/obj.data yolo-obj.cfg backup/yolo-obj_xxxx.weights**

## Testing

Refer to Link 2 in the above section to know when to stop training.

Once this is done, we can move on to testing. 

**Important - Open yolo-obj.cfg and change batch and subdivisions to 1, comment out the testing values**   

Save the .cfg file.  

Run `./darknet detector test data/obj.data yolo-obj.cfg backup/yolo-obj_xxxx.weights`  
By default, darknet will create a predictions.png file in darknet/ after it makes it's predictions. This will show all identified characters having a confidence value greater than the threshold (default is 0.25) with the bounding boxes. To run a test with a different threshold:  
`./darknet detector test data/obj.data yolo-obj.cfg backup/yolo-obj_xxxx.weights -thresh 0.x`  

This will yield results above the given threshold.


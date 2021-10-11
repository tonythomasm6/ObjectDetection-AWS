
from flask import Flask,request
import numpy as np
import sys
import time
import cv2
import os

#package for the json operations
import json
import io
import base64

#neccessary package to process image
from imageio import imread

# construct the argument parse and parse the arguments
confthres = 0.3
nmsthres = 0.1

def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on
    lpath=os.path.sep.join([yolo_path, labels_path])

    print(yolo_path)
    LABELS = open(lpath).read().strip().split("\n")
    return LABELS


def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([yolo_path, weights_path])
    return weightsPath

def get_config(config_path):
    configPath = os.path.sep.join([yolo_path, config_path])
    return configPath

def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net

def do_prediction(image,net,LABELS):

    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    #print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # ensure at least one detection exists
    arr=[]
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        #Converting the response into array of json
        for i in idxs.flatten():
            jsonObj = {}
            jsonObj['label'] = LABELS[classIDs[i]]
            jsonObj['accuracy'] = confidences[i]
            
            jsonDimension = {}
            jsonDimension['height'] = boxes[i][3]
            jsonDimension['left'] = boxes[i][0]
            jsonDimension['top'] = boxes[i][1]
            jsonDimension['width'] = boxes[i][2]
            jsonObj['rectangle'] = jsonDimension
            arr.append(jsonObj)
    return arr 


## Validating if input argument is correct
if len(sys.argv) != 2:
    raise ValueError("Argument list is wrong. Please use the following format:  {} {}".
                     format("python iWebLens_server.py", "<yolo_config_folder>"))

yolo_path  = str(sys.argv[1])

## Yolov3-tiny versrion
labelsPath= "coco.names"
cfgpath= "yolov3-tiny.cfg"
wpath= "yolov3-tiny.weights"

Lables=get_labels(labelsPath)
CFG=get_config(cfgpath)
Weights=get_weights(wpath)


#webservice using flas
app = Flask(__name__)
#Post request using api/objectdetection as url path
@app.route('/api/objectdetection', methods=['POST'])
def main():
    try:
        request_data = request.json             # Receiving request data from request
        imageIn = request_data.get('image')     # Getting base64 encoded image
        id = request_data.get('id')             # Getting image id
        npimg=imread(io.BytesIO(base64.b64decode(imageIn)))# Decoding image
        image=npimg.copy()
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # load the neural net. 
        nets = load_model(CFG, Weights)
        resultObject = do_prediction(image, nets, Lables)
        result = {}                             # Initializing json object to return
        result['object'] = resultObject        # Adding result json array with key as objects
        result['id']= id                        # Sending received id
        response = app.response_class(          # Converting json image into response object.
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        return response


    except Exception as e:
        print("Exception  {}".format(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)



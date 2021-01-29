import json
import os
import sys
import numpy as np
import pdb
import glob

from shutil import move
#from collections import defaultdict

usage_text = """
This script creates two coco annotation files by splitng it into two random parts

Usage: python data/scripts/mix_sets.py  train_path  val_path  ratio

ratio: training percentage
"""

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(usage_text)
        exit()
        
    train_path = sys.argv[1]
    val_path = sys.argv[2]
    ratio = sys.argv[3]
    
    with open(glob.glob(train_path + '/*.json')[0], 'r') as f:
        train_labels = json.load(f)
    
    nImages = len(train_labels["images"])

    # determine number of val images
    nVal = int(round(nImages*(1 - float(ratio))))
    print(nVal)
    # make random indices
    ind = np.random.permutation(nImages)
    valImages = np.asarray(train_labels["images"])[ind[0:nVal]]
    trainImages = np.asarray(train_labels["images"])[ind[nVal:]]

    valImages = valImages.tolist()
    trainImages = trainImages.tolist()

    train_annotations = []
    val_annotations = []
    train_id = 0
    val_id = 0
    
    prevID = -1
    isTrain = False

    for anno in train_labels["annotations"]:
        imgID = anno["image_id"]
        if imgID != prevID:
            if not imgID in ind[0:nVal]:
                newAnno = anno.copy()
                newAnno["id"] = train_id
                newAnno["image_id"] = int(np.where(ind == imgID)[0][0]) - nVal
                train_annotations.append(newAnno)
                train_id += 1
                prevID = imgID
                isTrain = True
                #pdb.set_trace()
            else:
                newAnno = anno.copy()
                newAnno["id"] = val_id
                newAnno["image_id"] = int(np.where(ind == anno["image_id"])[0][0])
                val_annotations.append(newAnno)
                val_id += 1
                prevID = imgID
                isTrain = False
        else:
            #pdb.set_trace()
            if isTrain:
                newAnno = anno.copy()
                newAnno["id"] = train_id
                newAnno["image_id"] = int(np.where(ind == anno["image_id"])[0][0]) - nVal
                train_annotations.append(newAnno)
                train_id += 1
                prevID = imgID
            else:
                newAnno = anno.copy()
                newAnno["id"] = val_id
                newAnno["image_id"] = int(np.where(ind == anno["image_id"])[0][0])
                val_annotations.append(newAnno)
                val_id += 1
                prevID = imgID


    
    #pdb.set_trace()

    # move val images
    for image in valImages:
        fileName = image["file_name"]
        move(os.path.join(train_path, fileName), os.path.join(val_path, fileName))
    
    train_labels["images"] = trainImages
    train_labels["annotations"] = train_annotations


    val_labels = train_labels.copy()
    val_labels["images"] = valImages
    val_labels["annotations"] = val_annotations

    #pdb.set_trace()
    # make image IDs ascending
    for i, im in enumerate(train_labels["images"]):
        #pdb.set_trace()
        im["id"] = i

            
    for j, im in enumerate(val_labels["images"]):
        #pdb.set_trace()
        im["id"] = j

    #pdb.set_trace()

    with open(os.path.join(train_path, 'test.json'), 'w+') as out_file:
        json.dump(train_labels, out_file)
    
    with open(os.path.join(val_path, 'test.json'), 'w+') as out_file:
        json.dump(val_labels, out_file)

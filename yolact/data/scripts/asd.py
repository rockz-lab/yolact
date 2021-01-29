import json

with open("annotations.json") as f:
    Data = json.load(f)


for anno in Data["annotations"]:
    anno["segmentation"] =  [anno["segmentation"].copy()]
    anno["image_id"] = int(anno["image_id"])

with open("annotations.json", 'w') as f:
    json.dump(Data, f)
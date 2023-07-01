import time
import cv2.dnn
import numpy as np

from ultralytics.yolo.utils import ROOT, yaml_load
from ultralytics.yolo.utils.checks import check_yaml

def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    color = (0, 0, 255)
    label = f'smoke (confidence: {confidence:.2f})'
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def detect(onnx_model, input_image):
    # COMMENT ##########
    framename = input_image
    input_image = "framesin/"+framename
    print(f"detecting {framename} ...")
    ####################
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(onnx_model)
    original_image: np.ndarray = cv2.imread(input_image)
    [height, width, _] = original_image.shape 
    length = max((height, width))
    image = np.zeros((length, length, 3), np.uint8)
    image[0:height, 0:width] = original_image
    scale = length / 640

    blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
    model.setInput(blob)
    outputs = model.forward()

    outputs = np.array([cv2.transpose(outputs[0])])
    rows = outputs.shape[1]

    boxes = []
    scores = []
    class_ids = []

    for i in range(rows):
        classes_scores = outputs[0][i][4:]
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
        if maxScore >= 0.25:
            box = [
                outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2], outputs[0][i][3]]
            boxes.append(box)
            scores.append(maxScore)
            class_ids.append(maxClassIndex)

    result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

    detections = []
    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        lefttopx = round(box[0] * scale)
        lefttopy = round(box[1] * scale)
        rightbtmx = round((box[0] + box[2]) * scale)
        rightbtmy = round((box[1] + box[3]) * scale)
        detection = {
                'class_id': class_ids[index],
                'confidence': scores[index],
                'rightbtmy': rightbtmy / height,
                'rightbtmx': rightbtmx / width,
                'lefttopy': lefttopy / height,
                'lefttopx': lefttopx / width
            }
        detections.append(detection)
        draw_bounding_box(original_image, class_ids[index], scores[index], 
                         lefttopx, lefttopy, rightbtmx, rightbtmy)
        
    # cv2.imwrite('outputimage.jpg', original_image)
    cv2.imwrite("framesout/"+framename, original_image) # COMMENT

    return detections

def detectsmoke(onnx_model, input_image):

    output_data = []
    
#     # 检测画面中是否有人（可以提高准确度但是很慢）
#     start = time.time()
#     detections = detect("v8coco.onnx", input_image)
#     detect_people = time.time() - start
#     person_detected = False
#     if len(detections) != 0: 
#         # something detected
#         for obj in detections:
#             if obj['class_id'] == 0: 
#                 person_detected = True
    
#     if person_detected:
    if True:
        # 检测画面中是否有吸烟
        detections = detect(onnx_model, input_image)
        if len(detections) != 0:
            # 检测到的每个烟
            for detection in detections:
                dat = {
                    'analysisType': 0, # 1:检测到吸烟, 0:未检测到吸烟
                    'score': detection['confidence'],
                    'imgUrl': None,
                    'coordinatesInfo': None,
                    '---rightBtmY': detection['rightbtmy'],
                    '---rightBtmX': detection['rightbtmx'],
                    '---leftTopY': detection['lefttopy'],
                    '---leftTopX': detection['lefttopx']
                }
                    
                output_data.append(dat)
        
    return output_data

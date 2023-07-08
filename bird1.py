import time
import numpy as np
from picamera2 import Picamera2, Preview
from PIL import Image
from tflite_runtime.interpreter import Interpreter
from email1 import Emailer

# init Raspberry Pi Camera
camera = Picamera2()
config_classifier = camera.create_still_configuration({"size": (224, 224)})
config_emailer = camera.create_still_configuration(buffer_count=2)

# specify paths to local file assets
path_to_labels_birds = "birds-label.txt"
path_to_labels = "labels_mobilenet_quant_v1_224.txt"
path_to_model_birds = "birds-model.tflite"
path_to_model = "mobilenet_v1_1.0_224_quant.tflite"

path_to_image_classifier = "images/bird.jpg"
path_to_image_emailer = "images/bird_hres.jpg"

# confidence threshold at which you want to be notified of a new bird
prob_threshold_bird = 0.9
prob_threshold_obj = 0.5

# Define email sender:
sender = Emailer()
sendTo = 'birdeye@myyahoo.com'


def main():
    """ Take a picture and see if a bird is in it """
    take_picture_classifier()
    take_picture_emailer()
    obj_check = check_for_object()
    bird_check = check_for_bird()

    if bird_check[0]:
        send_email(obj_check[1] + ' ' + bird_check[1])

    time.sleep(5)  # only check for birds every few seconds

def take_picture_classifier():
    """ Take a picture and save it """
    camera.configure(config_classifier)
    camera.start_preview(Preview.NULL)
    camera.start()
    time.sleep(2)  # give the camera 2 seconds to adjust light balance
    camera.capture_file(path_to_image_classifier)
    camera.stop_preview()
    camera.stop()

def take_picture_emailer():
    """ Take a picture and save it """
    camera.configure(config_emailer)
    camera.start_preview(Preview.NULL)
    camera.start()
    time.sleep(2)  # give the camera 2 seconds to adjust light balance
    camera.capture_file(path_to_image_emailer)
    camera.stop_preview()
    camera.stop()

def check_for_bird():
    """ Check if there is a bird in the image. """
    labels = load_labels_bird()
    interpreter = Interpreter(path_to_model_birds)
    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']

    image = Image.open(path_to_image_classifier)
    results = classify_image(interpreter, image, top_k = 5)
    label_id, prob = results[0]
    #print("bird: " + labels[label_id])
    #print("prob: " + str(prob))

    present = False
    bird = ''

    if prob > prob_threshold_bird:
        bird = labels[label_id]
        bird = bird[bird.find(",") + 1:]
        prob_pct = str(round(prob * 100, 1)) + "%"
        print("bird: " + bird)
        present = True

    return (present, bird)

def check_for_object():
    """ Check if there is an object in the image. """
    labels = load_labels()
    interpreter = Interpreter(path_to_model)
    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']

    image = Image.open(path_to_image_classifier)
    results = classify_image(interpreter, image, top_k = 5)
    label_id, prob = results[0]
    #print("bird: " + labels[label_id])
    #print("prob: " + str(prob))

    present = False
    object = ''

    if prob > prob_threshold_obj:
        object = labels[label_id]
        object = object[object.find(",") + 1:]
        prob_pct = str(round(prob * 100, 1)) + "%"
        print("object: " + object)
        present = True

    return (present, object)

def send_email(label_item):

    emailSubject = "object detected: " + label_item
    emailContent = "An object has been detected: " + time.ctime()
    sender.sendmail(sendTo, emailSubject, emailContent, path_to_image_emailer)

def load_labels():
    """ load labels for the ML model from the file specified """
    with open(path_to_labels, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}

def load_labels_bird():
    """ load labels for the ML model from the file specified """
    with open(path_to_labels_birds, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}

def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image


def classify_image(interpreter, image, top_k=1):
    """ return a sorted array of classification results """
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    # if model is quantized (uint8 data), then dequantize the results
    if output_details['dtype'] == np.uint8:
        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)

    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]


while True:
    main()

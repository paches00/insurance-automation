import os 
import time
import pandas as pd
from PIL import Image
import json
import random
import cv2
from matplotlib.pyplot import figure
from matplotlib import pyplot as plt
from datasets import load_metric

from detectron2.utils.visualizer import Visualizer
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.engine import default_argument_parser
from detectron2.engine import default_setup
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor

from transformers import TrOCRProcessor
from transformers import VisionEncoderDecoderModel


class Seq2Seq_Detectron:

    def __init__(self, input):
        self.input = input
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("./weights/tuned-seq2seqv1")

    def load_list_from_file(file_name):
        my_list = []
        with open(file_name, 'r') as file:
            for line in file:
                my_list.append(json.loads(line))
        return my_list

    def split_data(lst, split):
        n = len(lst)
        n_20_percent = int(n * 0.05)
        n_80_percent = n - n_20_percent
        test = random.sample(lst, n_20_percent)
        train = [item for item in lst if item not in test]
        if split == 'train':
            return train

        if split == 'test':
            return test

    # Function to register dataset in coco format for Detectron Model
    def register_dataset(name, dirname):
        df = Seq2Seq_Detectron.load_list_from_file('data/bounding-box.txt')
        new_classese = pd.read_csv('data/new_classes.csv')
        if name not in DatasetCatalog.list():
            DatasetCatalog.register(name, lambda: Seq2Seq_Detectron.split_data(df, 'train'))

        MetadataCatalog.get(name).set(
            thing_classes=list(new_classese['classes']), split='train', dirname= dirname
        )

    # Function to set-up configs of detectron
    def setup_detectron(args):
        cfg = get_cfg()
        cfg.DATASETS.TRAIN = ("new_docs_dataset_train",)
        cfg.merge_from_file(args.config_file)
        cfg.merge_from_list(args.opts)
        cfg.freeze()
        default_setup(cfg, args)
        return cfg

    # Function that predicts bounding boxes using detectron and saves crops in /bounding_box_images
    def predict_detectron(self):
        df = Seq2Seq_Detectron.load_list_from_file('data/bounding-box.txt')
        new_classese = pd.read_csv('data/new_classes.csv')
        parser = default_argument_parser()
        args = parser.parse_args("--config-file weights/tuned-detectronv2/config.yaml MODEL.WEIGHTS weights/tuned-detectronv2/model_final.pth".split())
        cfg = Seq2Seq_Detectron.setup_detectron(args)
        predictor = DefaultPredictor(cfg)

        # Create a directory to save the bounding box images
        if not os.path.exists('images/bounding_box_images'):
            os.makedirs('images/bounding_box_images')
        else:
            # Remove any existing files in the directory
            for file in os.listdir('images/bounding_box_images'):
                os.remove(os.path.join('images/bounding_box_images', file))

        files = []
        for dict in Seq2Seq_Detectron.split_data(df, 'test'):
            files.append(dict['file_name'])

        # Set sample size as wanted
        sample_size = 1

        im = cv2.imread(self.input)
        MetadataCatalog.get("new_docs_dataset_train").thing_classes = list(new_classese['classes'])
        start_time = time.time()
        outputs = predictor(im)
        print(time.time()- start_time)

        v = Visualizer(im[:, :, ::-1], metadata=MetadataCatalog.get("new_docs_dataset_train"), scale=1)
        instances = outputs["instances"].to("cpu")
        v = v.draw_instance_predictions(instances)

        # Save each bounding box as a .jpg file with its name being equal to the predicted class
        for i in range(len(instances)):
            class_name = MetadataCatalog.get("new_docs_dataset_train").thing_classes[instances.pred_classes[i]]
            bbox = instances.pred_boxes.tensor[i].cpu().numpy().astype(int)  # convert bounding box coordinates to integers
            box_image = im[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            cv2.imwrite(f'images/bounding_box_images/{class_name}.jpg', box_image)

        # Save image to file
        cv2.imwrite('images/result.jpg', v.get_image()[:, :, ::-1])


    # Retrieves sample from crops
    def retrieve_sample(self, path):
        image = Image.open('images/bounding_box_images/' + path).convert("RGB")
        # calling the processor is equivalent to calling the feature extractor
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        return image, pixel_values

    # Adds with specific key, the texto to its class
    def add_value_to_specific(df, column_to_check, value_to_check, column_to_add, value_to_add):
        df.loc[df[column_to_check] == value_to_check, column_to_add] = value_to_add
        return df

    # Predict with trOCR the written text in the images
    def predict_trocr(self):
        boxes = pd.DataFrame()
        files = []
        classes = pd.read_csv('data/new_classes.csv')
        boxes['classes'] = classes['classes'] 

        for file in os.listdir('images/bounding_box_images'):
            image, pixel_values = self.retrieve_sample(file)
            generated_ids = self.model.generate(pixel_values)
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            Seq2Seq_Detectron.add_value_to_specific(boxes, 'classes', file.split('.jpg')[0], 'texto', generated_text)
            print('Campo: ', file.split('.jpg')[0])
            print(generated_text)
        return boxes

    def run_model(self):
        self.predict_detectron()
        boxes = self.predict_trocr()
        return boxes
import pandas as pd
from PIL import Image
import os
import sys

# dimensions for 720p images
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

EXTRACTED_FRAMES_PATH = "./extracted_frames/"
SIGN_LABELS_PATH = "./sign_labels.txt"

OUTPUT_DIR = "annotation_files"

def validate_bounding_box(x_min, y_min, x_max, y_max, image_width, image_height):
    # negative min coordinates not allowed
    if x_min < 0 or y_min < 0:
        return False

    # max coordinates must be within image dimensions
    if x_max > image_width or y_max > image_height:
        return False
    
    # min coordinates must be smaller than max coordinates
    if x_min >= x_max or y_min >= y_max:
        return False

    return True


def create_sign_mapping(labels_path):
    # map sign labels to a numeric id equal to their line number in the labels file
    label_mapping = {}
    
    with open(labels_path, 'r') as f:
        for id, label in enumerate(f):
            label = label.strip()  # remove the newline at the end
            label_mapping[label] = id
            
    return label_mapping


def create_annotation_files(csv_path):
    df = pd.read_csv(csv_path)
    label_mapping = create_sign_mapping(SIGN_LABELS_PATH)

    frame_groups = df.groupby('frame_id')

    for frame_id, groups in frame_groups:
        frame_path = EXTRACTED_FRAMES_PATH + f"frame_{frame_id:05d}.png"

        # check if path is a valid file
        if not os.path.isfile(frame_path):
            print(f"Frame with id {frame_id} does not exist at path {frame_path}")
            continue

        # save all annotations for a frame in a list of strings
        annotation_lines = []

        for _, group in groups.iterrows():
            x_min = group['x_min']
            y_min = group['y_min']
            x_max = group['x_max']
            y_max = group['y_max']
            class_label = group['class_label']

            # check if bounding box on the current row is valid
            if not validate_bounding_box(x_min, y_min, x_max, y_max, FRAME_WIDTH, FRAME_HEIGHT):
                print(f"Invalid bounding box: {x_min}, {y_min}, {x_max}, {y_max} in frame {frame_id}")
                continue

            # calculate the center coordinates and bonding box width, and then
            # divide them by FRAME_WIDTH AND FRAME_HEIGHT to normalize values
            center_x = ((x_min + x_max) / 2) / FRAME_WIDTH
            center_y = ((y_min + y_max) / 2) / FRAME_HEIGHT
            width = (x_max - x_min) / FRAME_WIDTH
            height = (y_max - y_min) / FRAME_HEIGHT

            # add annotation line string for bounding box of the current frame
            # contains the sign label id and normalized bounding box coordintes
            annotation_lines.append(
                f"{label_mapping[class_label]} {center_x} {center_y} {width} {height}")

        if len(annotation_lines) > 0:
            annotation_file = os.path.join(OUTPUT_DIR, f"frame_{frame_id:05d}.txt")
            # write annotation lines to file
            with open(annotation_file, 'w') as f:
                for l in annotation_lines:
                    f.write(l + "\n")
        else:
            print(f"No valid bounding boxes for frame {frame_id}, no annotation file is created for it.")


def main():
    # check command line arguments
    if len(sys.argv) != 2:
        print("Usage: dataset_preparator.py <annotations_csv_path>")
        sys.exit(1)

    # fetch the command line argument
    annotations_csv_path = sys.argv[1]

    if not os.path.isfile(annotations_csv_path):
        print("Annotations CSV file does not exist")
        sys.exit(1)

    # create or replace output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # create annotation files and save them in directory
    create_annotation_files(annotations_csv_path)


if __name__ == "__main__":
    main()

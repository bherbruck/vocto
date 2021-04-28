import glob
import json
import os

import xmltodict
from PIL import Image

DATASET_DIR = './data'
OUTPUT_DIR = './data/output'
ANN_DIR = './data'  # TODO
IMG_DIR = './data'  # TODO


def get_dataset(directory=None):
    dataset_dir = directory or DATASET_DIR
    files = glob.glob(os.path.join(dataset_dir, '*.xml'))
    dataset = {'dataset_dir': dataset_dir,
               'annotations': [get_data(read_xml(file)) for file in files]}
    return dataset


def read_xml(path, convert=True):
    with open(path, 'r') as file:
        data = xmltodict.parse(file.read())
        return ordered_dict_to_dict(data) if convert else data


def ordered_dict_to_dict(ordered_dict):
    return json.loads(json.dumps(ordered_dict))


def get_data(ann_dict):
    root = ann_dict['annotation']
    data = {'filename': root['filename']}
    anns = clean_annotations(root)
    data['objects'] = [get_box(ann) for ann in anns]
    return data


def clean_annotations(element):
    anns = element.get('object')
    # wrap in a list if it is a dict
    return [anns] if isinstance(anns, dict) else anns or []


def get_box(element):
    data = {'name': element.get('name')}
    data.update(element.get('bndbox'))
    return data


def write_images(dataset, directory=None):
    output_dir = directory or OUTPUT_DIR
    mkdir_safe(output_dir)
    for ann in dataset['annotations']:
        img = Image.open(os.path.join(dataset['dataset_dir'],
                                      ann['filename']))
        for index, obj in enumerate(ann['objects']):
            write_dir = os.path.join(output_dir, obj['name'])
            mkdir_safe(write_dir)
            img_crop = img.crop((int(obj['xmin']), int(obj['ymin']),
                                 int(obj['xmax']), int(obj['ymax'])))
            filename, file_extension = os.path.splitext(ann['filename'])
            output_name = f'{filename}_{index}{file_extension}'
            img_crop.save(os.path.join(write_dir, output_name))
            print(f'Saving {output_name}')


def mkdir_safe(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


if __name__ == "__main__":
    write_images(get_dataset())

import sys
import json


def get_classes(classes_path):
    '''loads the classes'''
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names


def pick_class_number(name, class_names):
    if not name in class_names:
        return -1
    #assert name in class_names, 'invalid class name{}'.format(name)
    return class_names.index(name)


def calc_scale(iw, ih):
    return min(416/iw, 416/ih)


if __name__ == '__main__':
    scale_to_416x416 = False
    classes_path = 'dangerzone_classes.txt' #folder?
    class_names = get_classes(classes_path)
    json_file = sys.argv[1]
    # print(json_file)
    f = open(json_file, 'r')
    json_dict = json.load(f)
    scale = calc_scale(json_dict['imageWidth'],
                       json_dict['imageHeight'])
    str = "/mnt/data/public/imageDatabases/DangerZones/AllPhotos/" + \
        json_dict['imagePath'] #Photo path here
    for shape in json_dict['shapes']:
        x1 = round(shape['points'][0][0])
        x2 = round(shape['points'][1][0])  
        y1 = round(shape['points'][1][1])
        y2 = round(shape['points'][0][1])
        if x1 > x2:
            xmin = x2
            xmax = x1
        elif x2 > x1:
            xmin = x1
            xmax = x2
        if y1 > y2:
            ymin = y2
            ymax = y1
        elif y2 > y1:
            ymin = y1
            ymax = y2
        if scale_to_416x416:
            xmin = round(xmin*scale)
            ymin = round(ymin*scale)
            xmax = round(xmax*scale)
            ymax = round(ymax*scale)
        label = shape['label']
        label = pick_class_number(label, class_names)
        if label >= 0:
            str = str + \
                ' {},{},{},{},{}'.format(xmin, ymin, xmax, ymax, label)
    print(str)

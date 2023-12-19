###############################################################################
#
#   Authors: Erik Tjong Kim Sang & Lisa Hoek
#   Links:   https://github.com/ree-hdsc/ree-hdsc
#            https://github.com/LisaHoek/HANDS-RX
#
###############################################################################

import ast, json, os, re
import numpy as np
import xml.etree.ElementTree as ET

def get_text_from_file(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    full_text, info, metadata = get_text_from_xml(root)
    textregions = get_textregions_from_xml(root)
    return full_text, info, metadata, textregions

def get_value_string(fields):
    value_string = fields.pop(0)
    while fields and not re.search("}$", value_string):
        value_string += fields.pop(0)
    return value_string

def string_to_dict(string):
    string = re.sub("^{", "", string)
    string = re.sub(";}$", "", string)
    pairs = string.split(";")
    data = {}
    for pair in pairs:
        pair_data = pair.split(":")
        data[pair_data[0]] = pair_data[1]
    return data

def process_custom_attrib(custom_line):
    fields = custom_line.split()
    data = {}
    while fields:
        key = fields.pop(0)
        if not fields:
            data[key] = []
        else:
            value_string = string_to_dict(get_value_string(fields))
            if key in data:
                data[key].append(value_string)
            else:
                data[key] = [value_string]
    return data

def process_textline_attrib(attribs):
    for attrib in attribs:
        if attrib == "custom":
            return process_custom_attrib(attribs[attrib])

def add_length_to_offset(metadata_value, text_length):
    for key in metadata_value:
        if key == "offset":
            metadata_value[key] = int(metadata_value[key]) + text_length
    return metadata_value

def expand_metadata(metadata_base, metadata_new, text_length):
    for key in metadata_new:
        if key in metadata_base:
            for value in metadata_new[key]:
                metadata_base[key].append(add_length_to_offset(value, text_length))
        else:
            metadata_base[key] = []
            for value in metadata_new[key]:
                metadata_base[key].append(add_length_to_offset(value, text_length))

def get_text_from_xml(root):
    full_text = ""
    avgs, baselines, info = [], [], []
    metadata = {}
    problem_counter = 0
    
    for textline in root.findall(".//{*}TextLine"):
        expand_metadata(metadata, process_textline_attrib(textline.attrib), len(full_text))
        
        # get baseline coordinates and its average
        baseline = textline.find("./{*}Baseline")
        parsed_baseline = []
        for coords in baseline.get('points').split(" "):
            coord_x = int(coords.split(",")[0])
            coord_y = int(coords.split(",")[1])
            parsed_baseline.append((coord_x, coord_y))
        baselines.append(parsed_baseline)
        avg = (np.average(np.array(parsed_baseline), axis=0))
        avgs.append(avg)
            
        # append dict of textline, baseline and avg baseline
        unicode = textline.find("./{*}TextEquiv/{*}Unicode")
        if unicode.text != None:
            info.append({"text": unicode.text, "baseline": parsed_baseline, "avg": avg})
        else:
            info.append({"text": "", "baseline": parsed_baseline, "avg": avg})

    # two checks that swap baselines if the avg height difference is < 20 pxs and
    # the first baseline starts more to the right than the ending of the second baseline
    for idx in range(len(info)):
        if idx!=0 and info[idx]['avg'][1]-info[idx-1]['avg'][1] < 20 and info[idx-1]['baseline'][0][0] > info[idx]['baseline'][-1][0]:
            info[idx-1], info[idx] = info[idx], info[idx-1]
                
    for idx in range(len(info)):
        if idx!=0 and info[idx]['avg'][1]-info[idx-1]['avg'][1] < 20 and info[idx-1]['baseline'][0][0] > info[idx]['baseline'][-1][0]:
            info[idx-1], info[idx] = info[idx], info[idx-1]
    
    # check if there are still baselines in wrong ordering
    for idx in range(len(info)):
        if idx!=0 and info[idx]['avg'][1]-info[idx-1]['avg'][1] < 20 and info[idx-1]['baseline'][0][0] > info[idx]['baseline'][-1][0]:
            problem_counter+=1
    if problem_counter > 1:
        for name in root.findall("./{*}Page"):
                print("Still an incorrect baseline ordering in file:", name.get('imageFilename'))

    # return one string with newlines from the list of strings
    for text in info:
        if text['text'] is not None:
            full_text += (text['text']) + "\n"
            
    return full_text, info, metadata

def json_string_add_quotes(string):
    return re.sub("{ *", "{ '",
                re.sub(": *", "': '",
                    re.sub("; *", "', '",
                        re.sub("} *'", "} ",
                            re.sub("; *}", "' }", string)))))

def convert_to_lists_coords(coords):
    pairs = coords.split()
    x_coords = []
    y_coords = []
    for pair in pairs:
        x, y = pair.split(",")
        x_coords.append(int(x))
        y_coords.append(int(y))
    return x_coords, y_coords

def get_extreme_points_coords(coords):
    if coords == "":
        return 0, 0, 0, 0
    x_coords, y_coords = convert_to_lists_coords(coords)
    return min(x_coords), max(x_coords), min(y_coords), max(y_coords)

def get_textregions_from_xml(root):
    textregions = []
    for textregion in root.findall(".//{*}TextRegion"):
        for coords in textregion.findall("./{*}Coords"):
            textregions.append(coords.attrib["points"])
    return textregions

def print_with_color(string, color_code=1):
    print(f"\x1b[3{color_code}m{string}\x1b[m", end="")

def read_files(data_dir):
    full_texts, infos, metadata, textregions = ({}, {}, {}, {})
    for file_name in os.listdir(data_dir):
        if re.search(".xml$", file_name):
            file_id = file_name[:-4]
            try:
                full_texts[file_id], infos[file_id], metadata[file_id], textregions[file_id] = get_text_from_file(os.path.join(data_dir, file_name))
            except:
                print_with_color(f"error processing file {file_id}\n")
    return full_texts, infos, metadata, textregions
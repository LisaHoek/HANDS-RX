###############################################################################
#
#   Author:  Lisa Hoek
#   Project: HANDS-RX
#            https://github.com/LisaHoek/HANDS-RX
#
###############################################################################

import os, regex
from colorama import Fore
from functionsNamedgroups import *

###############################################################################
#
#   Functions to read and clean certificate texts and search for a match
#
###############################################################################

def clean_string(text):
    #text = text.replace('-\n', '')
    text = regex.sub(r"-\n(?=[a-z])", r"", text)
    text = regex.sub(r"-\n(?=[A-Z])", r"-", text)
    text = regex.sub(r"\n", " ", text)
    text = regex.sub(r"\s+", " ", text) # change to all whitespace characters, not only space
    return text

def read_certificates(path):
    certificates = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), mode='r', encoding='utf-8') as f:
            text = f.read()
            text = clean_string(text)
            certificates.append(text)
    return certificates

def pretty_print_certificate(match, text):
    indices = list(range(0,len(text)))
    for i in match.fuzzy_changes[2]:
        indices.insert(i, "_")
    for i in indices:
        if isinstance(i, int):
            if i in match.fuzzy_changes[0]:
                print(Fore.YELLOW, text[i], end='')
            elif i in match.fuzzy_changes[1]:
                print(Fore.RED, text[i], end='')
            else:
                if i >= match.span()[0] and i<=match.span()[1]:
                    print(Fore.GREEN, text[i], end='')
                else:
                    print(Fore.WHITE, text[i], end='')
        else:
            print(Fore.BLUE, i, end='')

def search_match(fuzzy_pattern, text, bool_print):
    match = regex.search(fuzzy_pattern, text, regex.BESTMATCH)
    if match and bool_print:
        print(match.groupdict())
        print(match.group())
        pretty_print_certificate(match, text)
        print('\n')
    elif match and not bool_print:
        print("Match.")
    else:
        print("No match.")

###############################################################################
#
#   Used to extract entities with RegExes
#
###############################################################################

# Function to get the tags from the metadata merged into one item
def get_tags(i, text, metadata, tag):
    tags = {}
    tag_parts = []
    if tag in metadata:
        for idx, item in enumerate(metadata[tag]):
            offset = int(item['offset'])
            length = int(item['length'])
            if idx>0 and int(metadata[tag][idx-1]['offset'])+int(metadata[tag][idx-1]['length'])+1 == offset: #combine outputs
                tag_parts[-1] = tag_parts[-1] + "\n" + text[offset:offset+length]
                tag_parts[-1] = clean_string(tag_parts[-1])
            else:
                tag_parts.append(clean_string(text[offset:offset+length]))
        tags[i] = tag_parts
    else:
        tags[i] = None
    return tags

# Return a list with all ids and a list with all labels (from get_tags)
def get_labels_from_metadata(texts, metadata, tag):
    ids, labels = [], []
    for i in texts:
        ids.append(i)
        if get_tags(i, texts[i], metadata[i], tag)[i] is None:
            labels.append(None)
        else:
            label_parts = get_tags(i, texts[i], metadata[i], tag)[i]
            labels.append(" ".join(label_parts))
    labels = [label.strip(" ,.") if label is not None else None for label in labels]
    return ids, labels

# From list to (e1|e2|e3) format
join_regex = lambda x: '(' + '|'.join(x) + ')'

# Create regex group with tag
def make_regex(named_group, group):
    return "(?P<"+named_group+">\\b" + join_regex(group) + "\\b)"

# Works for time, dates, sex, age
# From the found match, find the key that is the best match to obtain the value
def get_value_from_key_old(fuzzyness, entities, match, named_group, dict):
    better_found_matches = []
    for key in dict.keys():
        temp_regex = "(?b)^("+key+")$"
        fuzzy_pattern = f'({temp_regex}){{e<={fuzzyness}}}'
        temp = regex.search(fuzzy_pattern, match.group(named_group), regex.IGNORECASE)
        if temp:
            if len(better_found_matches) == 0 or better_found_matches[-1][1] > sum(temp.fuzzy_counts):
                better_found_matches.append((dict[key],sum(temp.fuzzy_counts)))
    print(better_found_matches[-1][0])
    entities.append(better_found_matches[-1][0])

def get_value_from_key(fuzzyness, match, named_group, dict):
    better_found_matches = []
    for key in dict.keys():
        temp_regex = "(?b)^("+key+")$"
        fuzzy_pattern = f'({temp_regex}){{e<={fuzzyness}}}'
        temp = regex.search(fuzzy_pattern, match.group(named_group), regex.IGNORECASE)
        if temp:
            if len(better_found_matches) == 0 or better_found_matches[-1][1] > sum(temp.fuzzy_counts):
                better_found_matches.append((dict[key],sum(temp.fuzzy_counts)))
    return better_found_matches[-1][0]

# Split the name of the deceased in first name(s) and last name
def split_name(name):
    if name is not None:
        name = name.strip()
        name = name.strip(",").strip(".")

        # If , take first part as last name and second part as first names
        if "," in name:
            name = name.split(",", 1)
            first_name = name[1].strip(" ,.")
            last_name = name[0].strip(" ,.")
        # If only 1 space, take first word as first name and last word as last name
        elif name.count(" ") == 1:
            name = name.split(" ", 1)
            first_name = name[0].strip(" ,.")
            last_name = name[1].strip(" ,.")
        # If multiple words
        else:
            name = name.split(" ")
            split_found = False
            # Check if there is a word lowercase (affix 'de' or 'van')
            while True:
                for idx, word in enumerate(name):
                    if word[0].islower():
                        # Take first parts as first name, take from lowercase to end as last name
                        first_name = (' '.join(word for word in name[:idx]).strip())
                        last_name = (' '.join(word for word in name[idx:]).strip())
                        split_found = True
                        break
                if split_found:
                    break  
                # If no lowercase is found, take only last word as last name and rest as first names 
                first_name = (' '.join(word for word in name[:-1]).strip())
                last_name = name[-1].strip(" ,.")
                split_found = True  
    else:
        first_name = None
        last_name = None
    return first_name, last_name

# Add 'ruim', 'circa' or 'naar gissing' to the age of the deceased
def add_age_estimate(subpart_singular, subpart_plural, subpart_parsing, age_nr, subpart_nr):
    if regex.search(f"(?e)(\bcirca\b){{e<=3}}.+({subpart_singular}|{subpart_plural})", subpart_parsing.group(), regex.IGNORECASE):
        age_nr.append("circa "+str(subpart_nr)+f" {subpart_singular}") if not subpart_plural in subpart_parsing.group() else age_nr.append("circa "+str(subpart_nr)+f" {subpart_plural}")
    elif regex.search(f"(?e)(\bruim\b){{e<=3}}.+({subpart_singular}|{subpart_plural})", subpart_parsing.group(), regex.IGNORECASE):
        age_nr.append("ruim "+str(subpart_nr)+f" {subpart_singular}") if not subpart_plural in subpart_parsing.group() else age_nr.append("ruim "+str(subpart_nr)+f" {subpart_plural}")
    elif regex.search(f"({subpart_singular}|{subpart_plural}).+(?e)(\bruim\b){{e<=3}}", subpart_parsing.group(), regex.IGNORECASE):
        age_nr.append(str(subpart_nr)+f" {subpart_singular}, ruim") if not subpart_plural in subpart_parsing.group() else age_nr.append(str(subpart_nr)+f" {subpart_plural}, ruim")
    elif regex.search(f"({subpart_singular}|{subpart_plural}).+(?e)(\bnaar gissing\b){{e<=3}}", subpart_parsing.group(), regex.IGNORECASE):
        age_nr.append(str(subpart_nr)+f" {subpart_singular}, naar gissing") if not subpart_plural in subpart_parsing.group() else age_nr.append(str(subpart_nr)+f" {subpart_plural}, naar gissing")
    else:
        age_nr.append(str(subpart_nr)+f" {subpart_singular}") if not subpart_plural in subpart_parsing.group() else age_nr.append(str(subpart_nr)+f" {subpart_plural}")

# change 'kwart over 2 's middags' to '14:15'
def parse_time(hour, match):
    time_entity = [hour, "00"]
    if "kwart over" in match.group():
        time_entity[1] = "15"
    if "te half" in match.group():
        time_entity[1] = "30"
        time_entity[0] = str(int(time_entity[0])-1)
    if "en een half" in match.group():
        time_entity[1] = "30"
    if "en een kwart" in match.group():
        time_entity[1] = "15"
    if "kwart voor" in match.group():
        time_entity[1] = "45"
        time_entity[0] = str(int(time_entity[0])-1)
    if ("namiddag" in match.group() or "na middag" in match.group() or "avond" in match.group()) and not time_entity[0] in ['12']:
        time_entity[0] = str(int(time_entity[0])+12)
    if "nacht" in match.group() and time_entity[0] in ['11', '10', '9']:
        time_entity[0] = str(int(time_entity[0])+12)
    if "nacht" in match.group() and time_entity[0] in ['12'] and not "half" in match.group() and not "kwart voor" in match.group():
        time_entity[0] = str(int(time_entity[0])-12)
    if time_entity[0] == "-1":
        time_entity[0] == "23"
    if time_entity[0] == "24":
        time_entity[0] == "0"
    time_entity = str(time_entity[0])+":"+time_entity[1]
    if len(time_entity) <= 4:
        time_entity = "0"+time_entity
    return time_entity


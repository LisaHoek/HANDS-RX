###############################################################################
#
#   Author:  Lisa Hoek
#   Project: HANDS-RX
#            https://github.com/LisaHoek/HANDS-RX
#
###############################################################################

import regex
from functionsNamedgroups import *
from functionsXML import *
from functions import *
import pandas as pd

# Specifies years as used in dates
year_expr = make_regex("hundreds", hundreds)+"\W{0,3}(en)?\W{0,3}("+make_regex("first10", first10)+"|"+make_regex("first10", first10)+"\W{0,3}(en)?\W{0,3}"+make_regex("tens", tens)+"|"+make_regex("second10", second10)+"|"+make_regex("tens", tens)+")"
year_expr_birth = make_regex("birth_hundreds", birth_hundreds)+"(\W{0,3}(en)?\W{0,3}("+make_regex("first10", first10)+"|"+make_regex("first10", first10)+"\W{0,3}(en)?\W{0,3}"+make_regex("tens", tens)+"|"+make_regex("second10", second10)+"|"+make_regex("tens", tens)+"))?"

###############################################################################
#
#   Certificate number
#
###############################################################################

certificate_number = "(?i)n[ro]\.? ?(?P<certificate_number>\d{1,4})\.?"

def find_certificate_number_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        match = regex.search(certificate_number, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            entity = match.group('certificate_number').strip(" ,.")
            if print_log in ['All']: print("ENTITY:\t", entity)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "CERTIFICATE_NUMBER":entity})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "CERTIFICATE_NUMBER":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Certificate district
#
###############################################################################

# Can be extracted from file_name
def find_certificate_district_in_texts(sample_name, texts, print_log):
    print("Not implemented.")
    return None

###############################################################################
#
#   Place of death
#
###############################################################################

place_of_death = "(?b)(dat in (?P<place_of_death>(\S+\W+){0,5}?)op den|(?P<place_of_death>alhier) is (ter|overleden))\\b"

def find_place_of_death_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        match = regex.search(place_of_death, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            entity = match.group('place_of_death').strip(" ,.")
            if print_log in ['All']: print("ENTITY:\t", entity)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "PLACE_OF_DEATH":entity})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "PLACE_OF_DEATH":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Place of birth
#
###############################################################################

place_of_birth = "(?b)geboren (en wonende )?((op|te)\W{0,3}(?P<place_of_birth>(\S+\W+)+?)|(?P<place_of_birth>alhier))\W{0,3}\\b(waarvan akte|datum|op|den|in het|en|"+make_regex("sex", sex)+")\\b"

def find_place_of_birth_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        match = regex.search(place_of_birth, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            entity = match.group('place_of_birth').strip(" ,.")
            if regex.search("cura.ao", entity, regex.IGNORECASE):
                entity = "Curaçao"
            if print_log in ['All']: print("ENTITY:\t", entity)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "PLACE_OF_BIRTH":entity})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "PLACE_OF_BIRTH":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Profession of the deceased
#
###############################################################################

profession_subtext = "(?<=heden).+(?P<subtext>(overleden is|is overleden).+?("+make_regex("sex", sex)+"|\bgehuwd))"
profession_expr = "(?P<profession>zonder beroep)|(van beroep|in leven(?! van beroep)) (?P<profession>\S+?)\W+?|jaren\W+?(?P<profession>\S+?)(,| (alhier|geboren))"

def find_profession_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        match = regex.search(profession_subtext, example, regex.IGNORECASE)
        if match:
            subtext = match.group("subtext")
            match = regex.search(profession_expr, subtext, regex.IGNORECASE)
            if match:
                if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
                entity = match.group("profession").strip(" ,")
                if print_log in ['All']: print("ENTITY:\t", entity)
                lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "PROFESSION":entity})
            else:
                if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
                lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "PROFESSION":None})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO SUBTEXT MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "PROFESSION":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Marital status
#
###############################################################################

marital_status_regex = "(?b)(?<=(overleden|kind).+?)"+make_regex("marital_status", marital_status)

def find_marital_status_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        entity = None
        example = clean_string(texts[file_name])
        match = regex.search(marital_status_regex, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            if match.group("marital_status") is not None:
                entity = get_value_from_key(0,match,"marital_status",marital_status)
            if print_log in ['All']: print("\nENTITY:\t", entity)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "MARITAL_STATUS":entity})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "MARITAL_STATUS":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Sex of deceased
#
###############################################################################

# Needs better split which is solved if all stillborns are filtered out

sex_regex = "(?b)"+make_regex("sex", sex)

def find_sex_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        entity = None
        example = clean_string(texts[file_name])
        match = regex.search(sex_regex, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            if match.group("sex") is not None:
                entity = get_value_from_key(0,match,"sex",sex)
            if print_log in ['All']: print("ENTITY:\t", entity)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "SEX":entity})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "SEX":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Time of death
#
###############################################################################

day_part = '(ochtend|morgen|(voor|vóór|na)? ?middag|avond|nacht)s?'
time_options = ['(((kwart voor|kwart over|half) ?)?'+make_regex("hours", hours)+' ure des '+day_part,
           day_part+' ten? ((kwart voor|kwart over|half) )?'+make_regex("hours", hours)+' uur',
           make_regex("hours", hours)+' en een (kwart|half) (ure|uur) des '+day_part+')']
time_of_death_regex = "(?b)(ten?|des)\W{0,3}"+make_regex("time",time_options)

def find_time_of_death_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        match = regex.search(time_of_death_regex, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            if match.group("hours") is not None:
                hour = get_value_from_key(0,match,"hours",hours)
            time_entity = parse_time(hour, match)

            if print_log in ['All']: print("ENTITY:\t", time_entity)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "TIME_OF_DEATH":time_entity})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "TIME_OF_DEATH":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Informants (name+age+profession)
#
###############################################################################

informants_type1_subtext = "(de personen van).+?(de\s?welke)"
informants_type2_subtext = "(op cura.ao).+?(verklaarde)"

informants_type1_regex = "(?b)(de personen van)\W{0,3}(?P<name_informant_1>(\S+\W+)+?)(.+?overledene)?(van beroep)\W{0,3}(?P<profession_informant_1>(\S+\W+)+?)(oud)(?P<age_informant_1>.+? jaren).+?(\\ben\\b)\W{0,3}(?P<name_informant_2>(\S+\W+)+?)(.+?overledene)?(van beroep)\W{0,3}(?P<profession_informant_2>(\S+\W+)+?)(oud)(?P<age_informant_2>.+? jaren)"
informants_type2_regex = "(op cura.ao)\W{0,3}(?P<name_informant_1>(\S+\W+)+?)(oud)\W{0,3}(?P<age_informant_1>.+? jaren)\W{0,3}(?P<profession_informant_1>(\S+\W+)+?)(wonende)"

# transform the informant's age to digits
def age_informants_to_digits(year_nr, entity): 
    year_parsing = regex.search(year_options, entity, regex.IGNORECASE) 
    if year_parsing:
        if "honderd" in year_parsing.group():
            year_nr+=100
        if year_parsing.group("first10") is not None:
            year_nr+=get_value_from_key(0,year_parsing,"first10",first10)
        if year_parsing.group("tens") is not None:
            year_nr+=get_value_from_key(0,year_parsing,"tens",tens)
        if year_parsing.group("second10") is not None:
            year_nr+=get_value_from_key(0,year_parsing,"second10",second10)
        return str(year_nr)+" jaren"
    else:
        return None
    
def find_informants_in_texts(sample_name, texts, print_log):
    lst_informant_1, lst_informant_2 = [], []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        subtext1 = regex.search(informants_type1_subtext, example, regex.IGNORECASE)
        # Search for subtext_1
        if subtext1:
            match = regex.search(informants_type1_regex, subtext1.group(), regex.IGNORECASE)
            # Search for regex_1 in subtext_1
            if match:
                if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
                
                name = match.group("name_informant_1").strip(" ,.")
                name = regex.sub("\w+ (van den?|der) ((hier)?na ?te ?(be)?noemene? )?overledene", "", name).strip(" ,.")
                age = age_informants_to_digits(0, match.group("age_informant_1").strip(" ,."))
                profession = match.group("profession_informant_1").strip(" ,.")
                if print_log in ['All']: print("NAME:\t", name, "\nAGE:\t", age, "\nPROF:\t", profession)
                lst_informant_1.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "NAME_INFORMANT_1":name, "AGE_INFORMANT_1":age, "PROFESSION_INFORMANT_1":profession})

                name = match.group("name_informant_2").strip(" ,.")
                name = regex.sub("\w+ (van den?|der) ((hier)?na ?te ?(be)?noemene? )?overledene", "", name).strip(" ,.")
                age = age_informants_to_digits(0, match.group("age_informant_2").strip(" ,."))
                profession = match.group("profession_informant_2").strip(" ,.")
                if print_log in ['All']: print("NAME:\t", name, "\nAGE:\t", age, "\nPROF:\t", profession)
                
                lst_informant_2.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "NAME_INFORMANT_2":name, "AGE_INFORMANT_2":age, "PROFESSION_INFORMANT_2":profession})                
            # regex_1 not found in subtext_1
            else:
                if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
                lst_informant_1.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "NAME_INFORMANT_1":None, "AGE_INFORMANT_1":None, "PROFESSION_INFORMANT_1":None})
                lst_informant_2.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "NAME_INFORMANT_2":None, "AGE_INFORMANT_2":None, "PROFESSION_INFORMANT_2":None})
        # Search for subtext_2
        else:
            subtext2 = regex.search(informants_type2_subtext, example, regex.IGNORECASE)
            # Search for regex_2 in subtext_2
            if subtext2:
                match = regex.search(informants_type2_regex, subtext2.group(), regex.IGNORECASE)
                if match:
                    if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
                    name = match.group("name_informant_1").strip(" ,.")
                    name = regex.sub("\w+ (van den?|der) ((hier)?na ?te ?(be)?noemene? )?overledene", "", name).strip(" ,.")
                    age = age_informants_to_digits(0, match.group("age_informant_1").strip(" ,."))
                    profession = match.group("profession_informant_1").strip(" ,.")
                    if print_log in ['All']: print("NAME:\t", name, "\nAGE:\t", age, "\nPROF:\t", profession)
                    lst_informant_1.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "NAME_INFORMANT_1":name, "AGE_INFORMANT_1":age, "PROFESSION_INFORMANT_1":profession})
                    lst_informant_2.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "NAME_INFORMANT_2":"-", "AGE_INFORMANT_2":"-", "PROFESSION_INFORMANT_2":"-"})
                # regex_2 not found in subtext_2
                else:
                    if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
                    lst_informant_1.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "NAME_INFORMANT_1":None, "AGE_INFORMANT_1":None, "PROFESSION_INFORMANT_1":None})
                    lst_informant_2.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "NAME_INFORMANT_2":None, "AGE_INFORMANT_2":None, "PROFESSION_INFORMANT_2":None})
            # Both subtext_1 and subtext_2 not found
            else:
                if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO SUBTEXT MATCH--")
                lst_informant_1.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "NAME_INFORMANT_1":None, "AGE_INFORMANT_1":None, "PROFESSION_INFORMANT_1":None})
                lst_informant_2.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "NAME_INFORMANT_2":None, "AGE_INFORMANT_2":None, "PROFESSION_INFORMANT_2":None})
                
    return pd.DataFrame.from_records(lst_informant_1), pd.DataFrame.from_records(lst_informant_2)

###############################################################################
#
#   Certificate date
#
###############################################################################

certificate_date = "(?b)heden (den )?"+make_regex("days", days)+" "+make_regex("months", months)+"\W{0,3}(des jaars)?\W{0,3}"+year_expr+"\W{0,3}(verscheen|compareerde)"

def find_certificate_date_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        day, month, year = [], [], []
        match = regex.search(certificate_date, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            day.append(get_value_from_key(0,match,"days",days))
            if match.group("months") is not None:
                month.append(get_value_from_key(0,match,"months",months))
            if match.group("hundreds") is not None:
                year.append(get_value_from_key(0,match,"hundreds",hundreds))
            if match.group("tens") is not None:
                year.append(get_value_from_key(0,match,"tens",tens))
            if match.group("first10") is not None:
                year.append(get_value_from_key(0,match,"first10",first10))
            if match.group("second10") is not None:
                year.append(get_value_from_key(0,match,"second10",second10))
            parsed_date = str(sum(day))+"-"+str(sum(month))+"-"+str(sum(year))
            if print_log in ['All']: print("ENTITY:\t", parsed_date)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "CERTIFICATE_DATE":parsed_date})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "CERTIFICATE_DATE":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Date of death
#
###############################################################################

date_of_death = "(?b)op (den )?"+make_regex("days", days)+" ("+make_regex("months", months)+")\W{0,3}((des jaars\W{0,3})?"+year_expr+"|dezes jaars|)\W{0,3}(ten?|des)\W"

def find_date_of_death_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        day, month, year = [], [], []
        match = regex.search(date_of_death, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            day.append(get_value_from_key(0,match,"days",days))
            if match.group("months") is not None:
                month.append(get_value_from_key(0,match,"months",months))
            if match.group("hundreds") is not None:
                year.append(get_value_from_key(0,match,"hundreds",hundreds))
            if match.group("tens") is not None:
                year.append(get_value_from_key(0,match,"tens",tens))
            if match.group("first10") is not None:
                year.append(get_value_from_key(0,match,"first10",first10))
            if match.group("second10") is not None:
                year.append(get_value_from_key(0,match,"second10",second10))
            parsed_date = str(sum(day))+"-"+str(sum(month))+"-"+str(sum(year))
            if print_log in ['All']: print("ENTITY:\t", parsed_date)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "DATE_OF_DEATH":parsed_date})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "DATE_OF_DEATH":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Date of birth
#
###############################################################################

date_of_birth = "(?b)z(ij|y)nde geboren (op)?\W{0,3}(\S+\s+){0,3}(op)?\W{0,3}((den\W{0,3})?"+make_regex("days", days)+" "+make_regex("months", months)+"\W{0,3}(des jaars?)?\W{0,3}"+year_expr_birth+"|in( het jaar)? "+year_expr_birth+")\W{0,3}(datum onbekend\W{0,3})?en is hiervan"

def find_date_of_birth_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        day, month, year = [], [], []
        match = regex.search(date_of_birth, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            if match.group("days") is not None:
                day.append(get_value_from_key(0,match,"days",days))
            if match.group("months") is not None:
                month.append(get_value_from_key(0,match,"months",months))
            if match.group("birth_hundreds") is not None:
                year.append(get_value_from_key(0,match,"birth_hundreds",birth_hundreds))
            if match.group("tens") is not None:
                year.append(get_value_from_key(0,match,"tens",tens))
            if match.group("first10") is not None:
                year.append(get_value_from_key(0,match,"first10",first10))
            if match.group("second10") is not None:
                year.append(get_value_from_key(0,match,"second10",second10))
            parsed_date = str(sum(day))+"-"+str(sum(month))+"-"+str(sum(year))
            if print_log in ['All']: print("ENTITY:\t", parsed_date)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "DATE_OF_BIRTH":parsed_date})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "DATE_OF_BIRTH":None})
    return pd.DataFrame.from_records(lst_entity)

###############################################################################
#
#   Name and Profession of father, mother and partner
#
###############################################################################

# Proved to be too difficult to implement within 8 hours

def find_father_info_in_texts(sample_name, texts, print_log):
    print("Not implemented yet...")
    return None

def find_mother_info_in_texts(sample_name, texts, print_log):
    print("Not implemented yet...")
    return None

def find_partner_info_in_texts(sample_name, texts, print_log):
    print("Not implemented yet...")
    return None

###############################################################################
#
#   Father / Mother deceased
#
###############################################################################

# (Assumption) zoon van wijlen [father] and [mother]: mother_deceased = None
parents = r"(?<=\boverleden\b.+?)(zoon|dochter).+?(en is hiervan|z(y|ij)nde geboren|a[ck]te)"#+"|"+"een kind.+?(en is hiervan|a[ck]te)|ure des.+?bevallen"

parents_type1 = r"(?b)(zoon|dochter) van\W{0,3}(?P<father>(\S+\W+)+?)\W{0,3}(\ben\b( van)?)\W{0,3}(?P<mother>(\S+\W+)+?)\W{0,3}((beiden? )?(alhier )?wonende|(thans|laatsten) wonende|z(y|ij)nde geboren|waarvan akte)"
parents_type2 = r"(?b)(zoon|dochter) van\W{0,3}(?P<mother>(\S+\W+)+?)\W{0,3}((beiden? )?(alhier )?wonende|(thans|laatsten) wonende|z(y|ij)nde geboren|waarvan akte)"

def find_parents_deceased_in_texts(sample_name, texts, print_log):
    lst_parents = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        subtext = regex.search(parents, example, regex.IGNORECASE)
        # Search for subtext
        if subtext:
            father_deceased = None
            mother_deceased = None
            match = regex.search(parents_type1, subtext.group(), regex.IGNORECASE)
            # Search for type1 in subtext
            if match:
                if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
                # if father has deceased
                if regex.search("((beiden? )?overleden|wijlen)", match.group('father'), regex.IGNORECASE):
                    father_deceased = "Ovl"
                # if mother has deceased
                if regex.search("((beiden? )?overleden|wijlen)", match.group('mother'), regex.IGNORECASE):
                    mother_deceased = "Ovl"
                # if both has deceased
                if regex.search("(beiden? overleden)", match.group('mother'), regex.IGNORECASE):
                    father_deceased = "Ovl"
                    mother_deceased = "Ovl"
                if print_log in ['All']: print("FATHER_DECEASED:\t", father_deceased, "\nMOTHER_DECEASED:\t", mother_deceased)
                lst_parents.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "FATHER_DECEASED":father_deceased, "MOTHER_DECEASED":mother_deceased})

            # type1 not found in subtext, search type2
            else:
                match = regex.search(parents_type2, subtext.group(), regex.IGNORECASE)
                if match:
                    if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
                    # if mother has deceased
                    if regex.search("((beiden? )?overleden|wijlen)", match.group('mother'), regex.IGNORECASE):
                        mother_deceased = "Ovl"
                    if print_log in ['All']: print("FATHER_DECEASED:\t", father_deceased, "\nMOTHER_DECEASED:\t", mother_deceased)
                    lst_parents.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "FATHER_DECEASED":None, "MOTHER_DECEASED":mother_deceased})

                # both types were not found
                else:
                    if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
                    lst_parents.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "FATHER_DECEASED":None, "MOTHER_DECEASED":None})

        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO SUBTEXT MATCH--")
            lst_parents.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "FATHER_DECEASED":None, "MOTHER_DECEASED":None})
                
    return pd.DataFrame.from_records(lst_parents)

###############################################################################
#
#   Name of the deceased
#
###############################################################################

name = r"(?b)(?<=\bheden\b.+?)(overleden is|is overleden)\W+(?P<name>(\S+\W+)+?)(in den ouderdom|oud|(zonder|van) beroep|wonende)"

def find_name_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        match = regex.search(name, example, regex.IGNORECASE)
        if match:
            entity = match.group('name')
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group(), "\nENTITY:\t", entity)
            parsed_first_names, parsed_last_names = split_name(entity)
            if print_log in ['All']: print("\nFIRST_NAMES\t",parsed_first_names, "\nLAST_NAME\t",parsed_last_names)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "NAME":entity, "FIRST_NAMES":parsed_first_names, "LAST_NAME":parsed_last_names})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "NAME":None, "FIRST_NAMES":None, "LAST_NAME":None})
    return pd.DataFrame.from_records(lst_entity)


###############################################################################
#
#   Age of the deceased
#
###############################################################################

year_options = "(\w+\W{0,3})?((honderd\W{0,3}(en\W{0,3})?)?"+make_regex("first10", first10)+"|"+make_regex("first10", first10)+"\W{0,3}(en)?\W{0,3}"+make_regex("tens", tens)+"|"+make_regex("second10", second10)+"|"+make_regex("tens", tens)+") (jaren|jaar)(\W{0,3}\w+)?(\W{0,3}\w+)?"
month_options = "(\w+\W{0,3})?"+make_regex("month_numbers", month_numbers)+" maand(en)?(\W{0,3}\w+)?(\W{0,3}\w+)?"
day_options = "(\w+\W{0,3})?"+make_regex("days", days)+" dag(en)?(\W{0,3}\w+)?(\W{0,3}\w+)?"
long_month_options = "(\w+\W{0,3})?"+make_regex("days", days)+" maand(en)?(\W{0,3}\w+)?(\W{0,3}\w+)?"

age = "(?b)(levens?loos)|(?<=(heden|personen).+?)((?<=(in den ouderdom van|is overleden .+? oud)) (?P<age>.+?) (?=("+make_regex("sex", sex)+" |in leven|geboren|(on)?gehuwd|(alhier )?(wonend|gewoond)|zonder|van beroep|vermoedelijk|volgen)))"
    
def find_age_in_texts(sample_name, texts, print_log):
    lst_entity = []
    for idx, file_name in enumerate(texts):
        example = clean_string(texts[file_name])
        match = regex.search(age, example, regex.IGNORECASE)
        if match:
            if print_log in ['All']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t", match.group())
            if match.group() == "levenloos" or match.group() == "levensloos":
                entity = match.group()
                age_string = None
            else:
                entity = match.group('age').strip(" ,.")
                year_parsing = regex.search(year_options, entity, regex.IGNORECASE)
                month_parsing = regex.search(month_options, entity, regex.IGNORECASE)
                day_parsing = regex.search(day_options, entity, regex.IGNORECASE)
                year_nr, month_nr, day_nr = 0, 0, 0
                age_nr = []
                
                if year_parsing:
                    if "honderd" in year_parsing.group():
                        year_nr+=100
                    if year_parsing.group("first10") is not None:
                        year_nr+=get_value_from_key(0,year_parsing,"first10",first10)
                    if year_parsing.group("tens") is not None:
                        year_nr+=get_value_from_key(0,year_parsing,"tens",tens)
                    if year_parsing.group("second10") is not None:
                        year_nr+=get_value_from_key(0,year_parsing,"second10",second10)
                    add_age_estimate("jaar", "jaren", year_parsing, age_nr, year_nr)
                
                if month_parsing:
                    if month_parsing.group("month_numbers") is not None:
                        month_nr+=get_value_from_key(0,month_parsing,"month_numbers",month_numbers)
                    add_age_estimate("maand", "maanden", month_parsing, age_nr, month_nr)
                
                if len(age_nr) == 0:
                    long_month_parsing = regex.search(long_month_options, entity, regex.IGNORECASE)
                    if long_month_parsing:
                        if long_month_parsing.group("days") is not None:
                            month_nr+=get_value_from_key(0,long_month_parsing,"days",days)
                        add_age_estimate("maand", "maanden", long_month_parsing, age_nr, month_nr)
                
                if day_parsing:
                    if day_parsing.group("days") is not None:
                        day_nr+=get_value_from_key(0,day_parsing,"days",days)
                    add_age_estimate("dag", "dagen", day_parsing, age_nr, day_nr)
                    
                if len(age_nr) == 0:
                    age_string = None
                age_string = ""
                if len(age_nr) == 3: age_string = age_nr[0]+", "+age_nr[1]+" en "+age_nr[2]
                if len(age_nr) == 2: age_string = age_nr[0]+" en "+age_nr[1]
                if len(age_nr) == 1: age_string = age_nr[0]

            if print_log in ['All']: print("ENTITY:\t", entity)
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":match.group(), "AGE":age_string})
        else:
            if print_log in ['All', 'Non_matches']: print("\nID:\t",file_name, "\nTEXT:\t", example, "\nMATCH:\t --NO MATCH--")
            lst_entity.append({"DOCUMENT": sample_name, "ID":file_name, "TEXT":example, "MATCH":None, "AGE":None})
    return pd.DataFrame.from_records(lst_entity)
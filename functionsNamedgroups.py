###############################################################################
#
#   Author:  Lisa Hoek
#   Project: HANDS-RX
#            https://github.com/LisaHoek/HANDS-RX
#
###############################################################################

# Specifies the digits below 10 to create numbers
first10 = {
    "een": 1,
    "twee": 2, 
    "drie": 3, 
    "vier": 4, 
    "vijf": 5,
    "zes": 6, 
    "zeven": 7, 
    "acht": 8, 
    "negen": 9, 
}

# Specifies the digits 11-19
second10 = {
    "elf": 11, 
    "twaalf": 12, 
    "dertien": 13, 
    "veertien": 14, 
    "vijftien": 15,
    "zestien": 16,
    "zeventien": 17, 
    "achttien": 18, 
    "negentien": 19, 
}

# Specifies the digits 10,20,30... to create numbers
tens = {
    "tien": 10,
    "twintig": 20,
    "dertig": 30,
    "veertig": 40,
    "vijftig": 50,
    "zestig": 60,
    "zeventig": 70,
    "tachtig": 80,
    "negentig": 90,
}

# Specifies the century to create years like "achttien honderd" and "achttienhonderd negen en tachtig"
hundreds = {
    "achttien\W*honderd": 1800,
    "negentien\W*honderd": 1900,
    "een\W*duizend\W*acht\W*honderd": 1800,
    "een\W*duizend\W*negen\W*honderd": 1900, 
}

# Better hundreds but knowledge was not known yet when only looking at training data
birth_hundreds = {
    "zeventien\W{0,3}honderd": 1700,
    "achttien\W{0,3}honderd": 1800,
    "negentien\W{0,3}honderd": 1900,
    "een\W{0,3}duizend\W{0,3}zeven\W{0,3}honderd": 1700,
    "een\W{0,3}duizend\W{0,3}acht\W{0,3}honderd": 1800,
    "een\W{0,3}duizend\W{0,3}negen\W{0,3}honderd": 1900, 
    "1700": 1700,
    "1800": 1800,
    "1900": 1900,
}

# Specifies how many months old someone can be
month_numbers = {
    "een": 1,
    "twee": 2, 
    "drie": 3, 
    "vier": 4, 
    "vijf": 5,
    "zes": 6, 
    "zeven": 7, 
    "acht": 8, 
    "negen": 9, 
    "tien": 10,
    "elf": 11, 
}

# Specifies the hours in a day
hours = { 
    "een|één": 1, 
    "twee": 2, 
    "drie": 3, 
    "vier": 4, 
    "vijf": 5,
    "zes": 6, 
    "zeven": 7, 
    "acht": 8, 
    "negen": 9, 
    "tien": 10,
    "elf": 11,
    "twaalf": 12,
}

###############################################################################

# Specifies the written out days of a month
days = { 
    "een|eersten?": 1, 
    "twee(den?)?": 2, 
    "drie|derden?": 3, 
    "vier(den?)?": 4, 
    "vijf(den?)?": 5,
    "zes(den?)?": 6, 
    "zeven(den?)?": 7, 
    "acht(sten?)?": 8, 
    "negen(den?)?": 9, 
    "tien(den?)?": 10,
    "elf(den?)?": 11, 
    "twaalf(den?)?": 12, 
    "dertien(den?)?": 13, 
    "veertien(den?)?": 14, 
    "vijftien(den?)?": 15,
    "zestien(den?)?": 16,
    "zeventien(den?)?": 17, 
    "achttien(den?)?": 18, 
    "negentien(den?)?": 19, 
    "twintig(sten?)?": 20,
    "een ?en ?twintig(sten?)?": 21, 
    "twee ?en ?twintig(sten?)?": 22, 
    "drie ?en ?twintig(sten?)?": 23, 
    "vier ?en ?twintig(sten?)?": 24, 
    "vijf ?en ?twintig(sten?)?": 25,
    "zes ?en ?twintig(sten?)?": 26, 
    "zeven ?en ?twintig(sten?)?": 27, 
    "acht ?en ?twintig(sten?)?": 28, 
    "negen ?en ?twintig(sten?)?": 29, 
    "dertig(sten?)?": 30,
    "een ?en ?dertig(sten?)?": 31,
}

# Specifies the written out months in a year
months = {
    "januar(i|y|ij)": 1,
    "februar(i|y|ij)": 2,
    "maart": 3,
    "april": 4,
    "mei": 5,
    "jun(i|y|ij)": 6,
    "jul(i|y|ij)": 7,
    "augustus": 8,
    "september": 9,
    "o[kc]tober": 10,
    "november": 11,
    "december": 12,
}

###############################################################################

district = '(stads|eersten?|1(st)?e|tweeden?|2d?e|derden?|3e|vierden?|4e|vijfden?|5e)'

# Specifies words that can indicate the sex of the deceased person
sex = {
    "weduwnaar": "m",
    "weduwe": "v",
    "echtgenoot\\b": "m",
    "echtgenoote\\b": "v",
    "mannelijk": "m",
    "vrouwelijk": "v",
    "zoon": "m",
    "dochter": "v",
}

# Specifies words that indicate the marital status of the deceased person
marital_status = {
    "weduwnaar": "weduwnaar",
    "weduwe": "weduwe",
    "echtgenoot\\b": "gehuwd",
    "echtgenoote\\b": "gehuwd",
    "\\bgehuwd": "gehuwd",
    "ongehuwd": "ongehuwd"
}

###############################################################################


"""
Defining helper functions and loading data from pickles
"""
import pickle
import os
import sys
import re

# different fonts and Save/Cancel button width for different OS
if sys.platform == 'darwin':
    BTN_WIDTH = 14
    FONT_M = ('Arial', 15, 'normal')
    FONT_S = ('Arial', 14, 'normal')
    FONT_ITAL = ('Arial', 13, 'italic')
    FONT_BOLD = ('Arial', 15, 'bold')
else:
    BTN_WIDTH = 15
    FONT_M = ('Arial', 13, 'normal')
    FONT_S = ('Arial', 11, 'normal')
    FONT_ITAL = ('Arial', 11, 'italic')
    FONT_BOLD = ('Arial', 13, 'bold')


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    Amended. Original from http://stackoverflow.com/a/13790741
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(base_path, relative_path)


def process_region(region_name):
    """
    Helper function to shorten region's names (exclude parentheses)
    text (string), region's name with parentheses

    Returns short region's name without parentheses
    """
    pattern1 = re.compile('.+[(].*[)]$')
    pattern2 = re.compile('.+ '+chr(8212)+' .*$')

    if pattern2.search(region_name):
        return region_name.split(' '+chr(8212)+' ')[0]
    elif pattern1.search(region_name):
        return region_name.split(' (')[0]
    else:
        return region_name


def logic_decorator(option):
    """
    Updates pickle files given the filename as option to the decorator
    (accepts 'users', 'dept', or 'regions')
    """
    def the_decorator(func):
        """ The decorator itself """
        def wrapper(self, *args, **kwargs):
            """ Updates pickle files """
            func(self, *args, **kwargs)
            try:
                with open(resource_path(option + '.pkl'), 'wb') as tempfile:
                    pickle.dump(globals()[option], tempfile)
            except KeyError:
                print('Wrong decorator option, check the code')
                raise
        return wrapper
    return the_decorator


# import labels (en for English, ru for Russian)
with open(resource_path('labels_en.pkl'), 'rb') as datafile:
    labels = pickle.load(datafile)

# import users
with open(resource_path('users.pkl'), 'rb') as datafile:
    users = pickle.load(datafile)

# import directors of departments
with open(resource_path('dept.pkl'), 'rb') as datafile:
    dept = pickle.load(datafile)

# import regions
with open(resource_path('regions.pkl'), 'rb') as datafile:
    regions = pickle.load(datafile)

# import texts
with open(resource_path('text.pkl'), 'rb') as datafile:
    text = pickle.load(datafile)

# TEMP
settings = {
    'middlenames': True,
    'read_receipt': True,
    'importance': [True, 5],
}

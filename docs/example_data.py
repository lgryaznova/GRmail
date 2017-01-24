"""
Prepare all the data for GRmail.py, convert into pickles
"""
import pickle

# labels (en for English, ru for Russian)
labels_en = {
    'left_pane': 'Fill in the form',
    'username': 'Choose user',
    'legal_fwd': 'FWD to legal',
    'legal_cc': 'Inform legal function',
    'gr_cc': 'Copy to GR Director',
    'customer': "Enter customer's name",
    'region': 'Enter region',
    'deadline': 'Enter deadline',
    'reason': 'Enter reason',
    'attachment': 'Add attachments',
    'no_files': 'No files selected',
    'browse': 'Browse',
    'generate': 'Generate text',
    'right_pane': 'Letter section',
    'to': 'To:',
    'cc': 'CC:',
    'subject': 'Subject:',
    'send': 'Send',
    'exit': 'Exit',
    'main': '  Main  ',
    'error_recognise_date': 'Cannot recognize the deadline. \
Try DD.MM.YYYY format. ',
    'error_early_deadline': 'Deadline cannot be earlier than today. ',
    'error_region1': ': type 1 error.',
    'error_region2': ': type 2 error.',
    'error_region3': ': type 3 error.',
    'error_manual_processing': '\nRequires manual processing.',
    'error_no_attachment': 'Choose file(s) to attach. ',
    'error_empty_field': 'Fill in the field(s) marked red. ',
    'address_book': '  Address Book  ',
    'save': 'Save',
    'cancel': 'Cancel',
    'delete': 'Delete',
    'choose_to_modify': 'Choose an entry to modify',
    'add_user': 'Add user',
    'cf_directors': 'CF Dept',
    'add_region': 'Add region',
    'fullname': 'Full name',
    'email': 'Email',
    'user_signature': '          Signature',
    'no_user_edit': 'Choose user to edit',
    'empty_fields': 'All fields must be filled in',
    'user_exists': 'The user {0} already exists. For a new user choose \
a unique name or click "Save" button again to replace the existing user.',
    'confirm_user_delete': 'Are you sure you want to delete {0}? \
To confirm click on "Delete" button again.',
    'user_deleted': 'User {0} is deleted',
    'user_added': 'User {0} is added',
    'user_updated': 'User {0} is updated',
    'user_duplicate': 'User {0} already exists. Choose another name \
for user {1} or click "Save" again to save as {0}.',
    'edit_user_pane': 'Edit user',
    'add_user_pane': 'Add a new user',
    'firstname': 'First & middle names',
    'lastname': 'Last name',
    'edit_dept': 'Edit CF department',
    'no_dir_edit': 'Choose department to edit',
    'dir_updated': 'Information about {0} is updated',
    'region0': 'normal operations',
    'no_region_edit': 'Choose region to edit',
    'edit_region_pane': 'Edit region info',
    'add_region_confirm': 'Regions on the list are subjects of the \
Russian Federation in accordance with the Constitution. Make sure \
that you need to amend the list.',
    'add_region_pane': 'Add a new region',
    'region_exists': 'The region {0} is already on the list. \
For a new region choose a unique name or click "Save" button \
again to replace the existing region.',
    'confirm_reg_delete': 'Are you sure you want to delete {0}? \
To confirm click on "Delete" button again.',
    'region_deleted': 'Region {0} is deleted',
    'region_added': 'Region {0} is added',
    'region_updated': 'Region {0} is updated',
    'region_duplicate': 'Region {0} already exists. Choose another \
name for region {1} or click "Save" again to save as {0}.',
    'amend_regname_confirm': 'Are you sure you want to edit the name \
of the region {0}? Click "Save" again to confirm.\n\n',
    'use_middlename': 'Use middlenames',
}

with open('labels_en.pkl', 'wb') as f:
    pickle.dump(labels_en, f)


# users
users = {
    'Liubov Gryaznova': ['liubov.gryaznova@example.com', \
'Yours sincerely,\n\nLiubov Gryaznova\nGR Specialist\n\
Tele2 Russia'],
    'Tabby McTat': ['tabbycat@example.com',
'Best regards,\n\nTabby McTat the musical cat'],
    'Old MacDonald': ['oldmacdonald@example.com', \
'Cheers,\n\nOld MacDonald had a farm E-I-E-I-O!']
}

with open('users.pkl', 'wb') as f:
    pickle.dump(users, f)


# regions
regions={
    'Middle-earth': [2, None, None],
    'Neverland': [1, None, None],
    'Hogwarts': [0, 'Albus P.W.B. Dumbledore', 'hogwarts@example.com'],
    'Wonderland': [3, None, None],
}

with open('regions.pkl', 'wb') as f:
    pickle.dump(regions, f)

# dept
dept = {
    'gr': ['Smith John W.', 'gr@example.com'],
    'legal': ['Bond James W.', 'legal@example.com']
}

with open('dept.pkl', 'wb') as f:
    pickle.dump(dept, f)


# texts
text_en = {
    'subjText': 'letter from {0}: {1}',
    'subjTextRegion': 'letter from {0} ({1}): {2}',
    'urgent': 'URGENT ',
    'due': '(due {0}) ',
    'ourReply': 'Dear {0},\n\nWe received a letter from the Ministry \
concerning an appeal by {1} ({2}) about {3}. Our department is \
writing a reply.\n\nPlease send us information on \
coverage in the mentioned above area before {4}.\n\n\n{5}',
    'regionReply': 'Dear {0},\n\nWe received a letter from the Ministry \
concerning an appeal by {1} ({2}) about {3}. Please send a reply \
to the customer within 30-day period and provide our department \
with the copy of the signed letter.\n\n\n{4}',
    'regionLegalReply': 'Dear {0},\n\nWe received a letter from the Ministry \
concerning an appeal by {1} ({2}) about {3}. Please send a reply \
to the customer within 30-day period and provide our department \
with the copy of the signed letter. Note that the text of the reply must be \
agreed upon by the legal department.\n\n\n{4}',
    'legalReply': 'Dear {0},\n\nPlease find enclosed a letter from the Ministry \
concerning an appeal by {1} about {2}.\n\n\n{3}'
}

with open('text.pkl', 'wb') as f:
    pickle.dump(text_en, f)



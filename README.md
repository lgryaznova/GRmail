## GRmail ver.1.03

### Overview

GRmail is an application intended to generate standard emails for specified occasions. It was designed mostly for my personal purposes to automate my everyday activities, save my time and efforts, and to assist my colleagues with the same tasks as well. Another aim was to practice programming in Python, designing a simple cross-platform app with GUI and making it work on a Windows machine without admin privileges and Python installed.

### Requirements

GRmail works on Windows 7 and MacOS Sierra (the latter reveals some GUI imperfections not affecting functionality; these will be fixed in later releases). To use as a script, one must have Python 3 installed to execute it. It is also suitable for compilation into a Windows executive with PyInstaller (ver.3.2.1 was successfully used by the author), both as a one file bundle or one folder bundle, since all the necessary details of transformation are taken into consideration.

**Notes on PyInstaller usage:** One file bundle by PyInstaller would work but it would not store any amendments to the data. To be able to save changes to the data permanently, use one folder bundle.

### Miscellaneous

**IMPORTANT NOTE** Unfortunately, at the moment sending emails functionality is not yet implemented. Therefore the app only generates emails and the 'Send' button copies the subject and the body of the email into the clipboard. Sending emails directly from the app will be hopefully implemented in next releases.

File *example_data.py* is a script to produce example data for the app and pack it into pickle files. It is not needed for the work of the app. We include it in the repo as it demonstrates data structures used by GRmail app.

The example data includes mentions of errors of types 1, 2 and 3. This was done to depersonalize data; the real app has more descriptive labels as it utilizes this feature. Emails and names are imaginary as well.

Email templates use first name and middle name due to the fact that the app was written for Russian language emails. Therefore this feature was preserved to maintain the same code as in the original app.

### Changelog

*ver.1.03*

Sending emails through MS Outlook is now working. The application uses the MS Outlook account found on the local machine to send the email. If not found, raises the error and copies the topic and the body of the email for manual processing. Sending via alternative servers will be implemented in next releases.

Internal structure of the project is revised. Now start.py is used to launch the app. Settings tab is added; however, it's logic is not added yet (to be accomplished in the next release).

*ver.1.02*

Slight improvements to the code, PEP8 compliance.

*ver.1.01*

Added AddressBook tab with all functionality to edit, add or delete data (users, departments, regions). Editing email templates will be added later on. Since now only one folder bundle can be used with PyInstaller, otherwise the updates in data will not be stored.

*ver.1.00*

Basic version is released, only main window is available. Data editing is on the way.



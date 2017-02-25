"""
Data classes
"""
class DataClass(dict):
    """
    Base class. For users and regions
    """
    def __init__(self):
        #self.inner_dict = {}
        super().__init__(self)
        self._current = None

    def keys(self):
        return sorted(super().keys())

    @property
    def current(self):
        """Gets the current item (user, region)"""
        return self._current

    @current.setter
    def current(self, item):
        self._current = item

    # def get_item(self, key):
    #     """Returns a specified item"""
    #     return self.inner_dict[key]

    # def all_items(self):
    #     """Returns a sorted list of all items (users or regions)"""
    #     return sorted(self.inner_dict.keys())

    # def delete_item(self, key):
    #     """Deletes an item"""
    #     if key is not None:
    #         del self.inner_dict[key]

    def update_item(self, class_, key, *args, **kwargs):
        """
        Adds or updates an item of a dictionary of users or regions.

        class_ - class (User or Region)
        key - string, name of user or region, key in the dictionary
        """
        assert key == self._current or key not in self.keys()
        # key (name) is not changed
        if key == self._current:
            self[key].update(key, *args, **kwargs)
        # new non-duplicate key name
        elif key not in self.keys():
            if self._current is not None:
                del self[self._current]
            self[key] = class_(key, *args, **kwargs)

    def force_update(self, class_, key, *args, **kwargs):
        """
        Force updates an item of a dictionary of users or regions.

        class_ - class (User or Region)
        key - string, name of user or region, key in the dictionary
        """
        # edit section only
        if self._current is not None:
            del self[self._current]
        # suitable for both add and edit sections
        self[key] = class_(key, *args, **kwargs)

    def appeal(self, key, flag):
        """
        Returns firstname or firstname+middlename of the specified
        user depending on the setting.

        key - string, name of region, key of the internal dict
        flag - boolean, True if middlename is used, otherwise False
        """
        if flag:
            return (self[key].firstname + ' ' + self[key].middlename)
        else:
            return self[key].firstname


class User(object):
    """Describes a single user"""
    def __init__(self, name, email, signature):
        self._name = name
        self._email = email
        self._signature = signature
        self._server = None
        self._port = None
        self._ssl = False
        self._alt_email = None
        self._reply_to = False
        self._bcc_to_corp = False

    def update(self, name, email, signature):
        """Updates user info"""
        self._name = name
        self._email = email
        self._signature = signature

    def set_network(self, server, port, ssl, alt_email,
                    reply_to, bcc_to_corp):
        """Adds network settings for the user"""
        self._server = server
        self._port = port
        self._ssl = ssl
        self._alt_email = alt_email
        self._reply_to = reply_to
        self._bcc_to_corp = bcc_to_corp

    @property
    def name(self):
        """Get user's name"""
        return self._name

    @property
    def email(self):
        """Get email"""
        return self._email

    @property
    def signature(self):
        """Get signature"""
        return self._signature

    @property
    def server(self):
        """Get server"""
        return self._server

    @property
    def port(self):
        """Get port"""
        return self._port

    @property
    def ssl(self):
        """Get SSL flag"""
        return self._ssl

    @property
    def alt_email(self):
        """Get alternative email"""
        return self._alt_email

    @property
    def reply_to(self):
        """Get flag if reply should be sent to corporate email"""
        return self._reply_to

    @property
    def bcc_to_corp(self):
        """Get flag if BCC to corporate email should be sent"""
        return self._bcc_to_corp


class Users(DataClass):
    """All users of the app"""

    def set_network(self, key, server, port, ssl, alt_email,
                    reply_to, bcc_to_corp):
        """Set network info"""
        self[key].set_network(
            server, port, ssl, alt_email, reply_to, bcc_to_corp)


class Department(object):
    """Describes a department (GR or Legal)"""
    def __init__(self, dept, firstname, middlename, lastname, email):
        self._dept = dept
        self._firstname = firstname
        self._middlename = middlename
        self._lastname = lastname
        self._email = email

    def update(self, firstname, middlename, lastname, email):
        """Updates info"""
        self._firstname = firstname
        self._middlename = middlename
        self._lastname = lastname
        self._email = email

    @property
    def firstname(self):
        """Get firstname"""
        return self._firstname

    @property
    def middlename(self):
        """Get middlename"""
        return self._middlename

    @property
    def lastname(self):
        """Get lastname"""
        return self._lastname

    @property
    def email(self):
        """Get email"""
        return self._email


class Departments(DataClass):
    """Contains a dict of two departments (GR and Legal)"""

    def update_item(self, class_, key, *args, **kwargs):
        """
        Adds or updates an item of a dictionary of departments.
        Department names remain unchanged.

        class_ - class (User or Region)
        key - string, name of department, key in the dictionary
        """
        self[key].update(*args, **kwargs)


class Region(object):
    """Describes a single region"""
    def __init__(self, regname, regtype, firstname, middlename,
                 lastname, email):
        self._regname = regname
        self._regtype = regtype
        self._firstname = firstname
        self._middlename = middlename
        self._lastname = lastname
        self._email = email

    def update(self, regname, regtype, firstname=None, middlename=None,
               lastname=None, email=None):
        """Updates region info"""
        self._regname = regname
        self._regtype = regtype
        self._firstname = firstname
        self._middlename = middlename
        self._lastname = lastname
        self._email = email

    @property
    def regname(self):
        """Name of region"""
        return self._regname

    @regname.setter
    def regname(self, new):
        self._regname = new

    @property
    def regtype(self):
        """Type of region"""
        return self._regtype

    @regtype.setter
    def regtype(self, new):
        self._regtype = new

    @property
    def firstname(self):
        """Firstname of regional director"""
        return self._firstname

    @firstname.setter
    def firstname(self, new):
        self._firstname = new

    @property
    def middlename(self):
        """Middlename of regional director"""
        return self._middlename

    @middlename.setter
    def middlename(self, new):
        self._middlename = new

    @property
    def lastname(self):
        """Lastname of regional director"""
        return self._lastname

    @lastname.setter
    def lastname(self, new):
        self._lastname = new

    @property
    def email(self):
        """Email of regional director"""
        return self._email

    @email.setter
    def email(self, new):
        self._email = new


class Regions(DataClass):
    """Describes full set of regions"""

    def update_item(self, class_, key, *args, **kwargs):
        """
        Adds or updates an item of a dictionary of regions.
        Request confirmation if the region's name is to be changed.

        class_ - class (User or Region)
        key - string, name of region, key in the dictionary
        """
        assert key == self._current
        super().update_item(class_, key, *args, **kwargs)


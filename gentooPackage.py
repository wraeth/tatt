"""Module for easy access to portage's atom syntax """

import re

class gentooPackage(object):
    """A Gentoo package consists of:
       category
       name
       version
    of a Gentoo package"""
    
    def __init__(self, st):
        """An atom is initialized from an atom string"""
        slashparts = st.split("/")
        self.category = slashparts[0]
        minusparts = slashparts[1].split("-")
        self.name = ""
        while 1:
            p = minusparts.pop(0)
            # Try a number after a '-'
            if re.match('[0-9]+', p):
                # Version starts here:
                self.ver = "-".join([p] + minusparts)
                break
            else:
                # Append back to name
                if self.name=="": self.name = p
                else : self.name = "-".join([self.name, p])


    def packageString(self):
        """ Returns a portage compatible string representation"""
        if self.ver == '':
            return  "/".join([self.category, self.name])
        else:
            return ( "=" + "/".join([self.category, "-".join([self.name, self.ver])]))


#| This file is part of pyCAF.                                               |
#|                                                                           |
#| pyCAF is free software: you can redistribute it and/or modify             |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| pyCAF is distributed in the hope that it will be useful,                  |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |    

# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 15:12:01 2014

@author: thierry
"""


class ACLtable():
    """@brief ACL table is a collection of ACL lists

    @param dict : dictionnary {name, ACLlist()}
    @param counter : number of ACLList in the dictionnary

    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_acl_list(self, name, acl_list):
        """
        Add an ACL list at the dictionnary
        Dictionnary model : [name,ACLlist]
        @param name : the acl to store
        """
        if name not in self.dict.keys():
            self.dict[name] = acl_list
            self.counter += 1
        else:
            print "ACL list name ever stored in the dictionnary"

    def get_acl_list(self, name):
        """
        Return an acl corresponding to the name
        @param ident : the number corresponding to the acl
        """
        if name in self.dict.keys():
            return self.dict[name]
        else:
            print "ACL list name not found"

    def __str__(self):
        """
        Print the caracteristics of the ACL table
        """

        for key, val in self.dict.items():
            print str(key),
            print val
        return ""

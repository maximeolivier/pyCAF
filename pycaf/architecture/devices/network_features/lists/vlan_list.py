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
Created on Mon Aug  4 10:38:39 2014

@author: thierry
"""

import pycaf.tools as tools

class VlanList():
    """Definition of what a VlanList is
    An vlan list is an object use for manage multiple vlan into a network device
    This class uses a dictionnary and a ident number is given at each vlan added.
    User can get a vlan with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_vlan(self, vlan):
        """
        Add a vlan at the network device dictionnary
        Dictionnary model : [counter,vlan]
        @param vlan : the vlan to store
        """
        self.counter += 1
        self.dict[self.counter] = vlan
        
    def get_vlan(self, ident):
        """
        Return a vlan corresponding to the ident value
        @param ident : the number corresponding to the vlan
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "vlan not found"
            
    def filter_vlan(self,*args, **kwargs):
        """
        Filter all vlan if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_vlan(4,6,8,...)
            
        Return accounts with specific values :
            filter_vlan(keyword="arg", keword2="arg2",....)
        keywords available :
        - number
        - name
        
        example : filter_vlan(name="admin42")
        
        Black list some users
        keyword :
        - hide_number
        - hide_name
        
        example 1 : filter_vlan(hide_number="12, 9")
        """
        list_filtered = VlanList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_vlan(elem)

        return list_filtered
            
    def show_vlan(self,*args, **kwargs):
        """
        Show all ACL if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_vlan(4,6,8,...)
            
        Return accounts with specific values :
            filter_vlan(keyword="arg", keword2="arg2",....)
        keywords available :
        - number
        - name
        
        example : filter_vlan(name="admin42")
        
        Black list some users
        keyword :
        - hide_number
        - hide_name
        
        example 1 : filter_vlan(hide_number="12, 9")
        """
        list_filtered = self.filter_vlan(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered

    def label_vlan_list(self):
        return "\n%s%s" %("VLAN".ljust(8), "Name".ljust(40))
        
    def __str__(self):
        """
        Print the list of vlan with their ident
        """
        print self.label_vlan_list()
        for identityNb, vlan in self.dict.items():
            print "{}".format(vlan),
            print identityNb
        return ""
        

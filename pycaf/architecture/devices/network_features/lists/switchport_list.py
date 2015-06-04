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
Created on Fri Aug  1 16:36:50 2014

@author: thierry
"""
import pycaf.tools as tools

class SwitchportList():
    """Definition of what a SwitchportList is
    An switchport list is an object use for manage multiple switchports into a network device
    This class uses a dictionnary and a ident number is given at each switchport added.
    User can get a switchport with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_switchport(self, switchport):
        """
        Add a switchport at the network device dictionnary
        Dictionnary model : [counter,switchport]
        @param switchport : the switchport to store
        """
        self.counter += 1
        self.dict[self.counter] = switchport
        
    def get_switchport(self, ident):
        """
        Return a switchport corresponding to the ident value
        @param ident : the number corresponding to the switchport
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "switchport not found"
            
    def filter_switchport(self,*args, **kwargs):
        """
        Filter all switchport if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_switchport(4,6,8,...)
            
        Return accounts with specific values :
            filter_switchport(keyword="arg", keword2="arg2",....)
        keywords available :
        - interface
        - active : warning, integer value : idle(0), standard(1) and extended(2)
        - description
        - vlan
        - vlan_allowed
        - mode
        
        example : filter_switchport(interface="GigabitEthernet3/0/24", active=True)
        
        Black list some users
        keyword :
        - hide_interface
        - hide_active : warning, integer value : idle(0), standard(1) and extended(2)
        - hide_description
        - hide_vlan
        - hide_vlan_allowed
        - hide_mode
        example 1 : filter_switchport(hide_vlan="12")
        """
        list_filtered = SwitchportList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_switchport(elem)

        return list_filtered
            
    def show_switchport(self,*args, **kwargs):
        """
        Show all switch if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_switchport(4,6,8,...)
            
        Return accounts with specific values :
            filter_switchport(keyword="arg", keword2="arg2",....)
        keywords available :
        - interface
        - active : warning, integer value : idle(0), standard(1) and extended(2)
        - description
        - vlan
        - vlan_allowed
        - mode
        
        example : filter_switchport(interface="GigabitEthernet3/0/24", active=True)
        
        Black list some users
        keyword :
        - hide_interface
        - hide_active : warning, integer value : idle(0), standard(1) and extended(2)
        - hide_description
        - hide_vlan
        - hide_vlan_allowed
        - hide_mode
        example 1 : filter_switchport(hide_vlan="12")
        """
        list_filtered = self.filter_switchport(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered

    def label_switchport_list(self):
        return "\n%s%s%s%s%s%s" %("Interface".ljust(30),\
            "Active".ljust(10), "VLAN".ljust(10), "VLAN allowed".ljust(35), "Mode".ljust(20), "Description".ljust(30))

    def __str__(self):
        """
        Print the list of accounts with their ident
        """
        print self.label_switchport_list()
        for identityNb, switchport in self.dict.items():
            print "{}".format(switchport),
            print identityNb
        return ""
        

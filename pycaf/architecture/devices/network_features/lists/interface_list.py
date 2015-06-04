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
Created on Fri Aug  1 16:00:49 2014

@author: thierry
"""
import pycaf.tools as tools

class InterfaceList():
    """Definition of what an InterfaceList is
    An interface list is an object use for manage multiple interfaces into a network device
    This class uses a dictionnary and a ident number is given at each interface added.
    User can get an interface with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_interface(self, interface):
        """
        Add an interface at the network device dictionnary
        Dictionnary model : [counter, interface]
        @param interface : the interface to store
        """
        self.counter += 1
        self.dict[self.counter] = interface
        
    def get_interface(self, ident):
        """
        Return an interface corresponding to the ident value
        @param ident : the number corresponding to the interface
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "interface not found"
            
    def filter_interface(self,*args, **kwargs):
        """
        Filter all interfaces if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_interface(4,6,8,...)
            
        Return accounts with specific values :
            filter_interface(keyword="arg", keword2="arg2",....)
        keywords available :
        - interface
        - name
        - active : warning True of False
        - ip
        - mask 
        - urpf : warning True of False
        - acl_list_in
        - acl_list_out
        
        example : filter_interface(mask="255.255.0.0", active=True)
        
        Black list some users
        keyword :
        - hide_interface
        - hide_name
        - hide_active : warning True of False
        - hide_ip
        - hide_mask 
        - hide_urpf : warning True of False
        - hide_acl_list_in
        - hide_acl_list_out
        example 1 : filter_interface(hide_mask="255.255.0.0")
        """
        list_filtered = InterfaceList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_interface(elem)

        return list_filtered
            
    def show_interfaces(self,*args, **kwargs):
        """
        Show all interfaces if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_interface(4,6,8,...)
            
        Return accounts with specific values :
            filter_interface(keyword="arg", keword2="arg2",....)
        keywords available :
        - interface
        - name
        - active : warning True of False
        - ip
        - mask 
        - urpf : warning True of False
        - acl_list_in
        - acl_list_out
        
        example : filter_interface(mask="255.255.0.0", active=True)
        
        Black list some users
        keyword :
        - hide_interface
        - hide_name
        - hide_active : warning True of False
        - hide_ip
        - hide_mask 
        - hide_urpf : warning True of False
        - hide_acl_list_in
        - hide_acl_list_out
        example 1 : filter_interface(hide_mask="255.255.0.0")
        """
        list_filtered = self.filter_interface(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered

    def label_interface_list(self):        
        return "\n%s%s%s%s%s%s%s" %("Name".ljust(30),\
        "Active".ljust(10), "IP address".ljust(18), "Mask".ljust(18), "uRPF".ljust(10),\
        "ACL List IN".ljust(20), "ACL List OUT".ljust(20))

    def __str__(self):
        """
        Print the list of accounts with their ident
        """
        print self.label_interface_list()
        for identityNb, iface in self.dict.items():
            print "{}".format(iface),
            print identityNb
        return ""
        

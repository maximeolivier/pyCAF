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

class InterfaceList():
    """
    Class wich create a list of interfaces
    Definition of what an interface  is
    An interface list is an object use for manage multiple interface into a server
    This class uses a dictionnary and a ident number is given at each interface added.
    User can get a interface with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter=0

    def add_interface(self, interface):
        """
        Add a interface at the server dictionnary
        Dictionnary model : [counter,interface]
        """
        self.counter += 1
        self.dict[self.counter]=interface
        
    def get_interface(self,ident):
        """
        Return a interface corresponding to the ident value
        @param ident : the number corresponding to the interface
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "interface not found"

    def label_interface_list(self):
        return "\n%s%s%s%s%s\n" %("name".ljust(50), "ip address".ljust(18), "mask".ljust(18),\
        "mac adress".ljust(20), "ipv6 address".ljust(40))
    
    def __str__(self):
        """
        Print the list of interfaces with their ident
        """
        print self.label_interface_list()
        
        for identityNb, iface in self.dict.items():
            print "{}".format(iface),
            print identityNb
        return ""

        
        
        
        
        
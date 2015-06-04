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
Created on Mon Aug  4 17:47:20 2014

@author: thierry
"""

import pycaf.tools as tools

class RouteList():
    """Definition of what an routelist is
    A route list is an object use for manage multiple route into a network device
    This class uses a dictionnary and a ident number is given at each route added.
    User can get an route with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_route(self, route):
        """
        Add a route at the network device dictionnary
        Dictionnary model : [counter,route]
        @param route : the route to store
        """
        self.counter += 1
        self.dict[self.counter] = route
        
    def get_route(self, ident):
        """
        Return a route corresponding to the ident value
        @param ident : the number corresponding to the route
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "route not found"
            
    def filter_route(self,*args, **kwargs):
        """
        Filter all route if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_route(4,6,8,...)
            
        Return accounts with specific values :
            filter_route(keyword="arg", keword2="arg2",....)
        keywords available :
        - destination
        - mask
        - interface
        
        example : filter_route(mask="255.255.254.0", interface="10.10.1.42")
        
        Black list some users
        keyword :
        - hide_destination
        - hide_mask
        - hide_interface
        example 1 : filter_route(hide_interface="192.168.1.42")
        """
        list_filtered = RouteList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_route(elem)

        return list_filtered
            
    def show_route(self,*args, **kwargs):
        """
        Show all route if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_route(4,6,8,...)
            
        Return accounts with specific values :
            filter_route(keyword="arg", keword2="arg2",....)
        keywords available :
        - destination
        - mask
        - interface
        
        example : filter_route(mask="255.255.254.0", interface="10.10.1.42")
        
        Black list some users
        keyword :
        - hide_destination
        - hide_mask
        - hide_interface
        example 1 : filter_route(hide_interface="192.168.1.42")
        """
        list_filtered = self.filter_route(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered

    def label_route_list(self):
        return "\n%s%s%s\n" %("Destination".ljust(20), "Mask".ljust(20), "Interface".ljust(20))

    def __str__(self):
        """
        Print the list of accounts with their ident
        """
        print self.label_route_list()
        for identityNb, route in self.dict.items():
            print "{}".format(route),
            print identityNb
        return ""

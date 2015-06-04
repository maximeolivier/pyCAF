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
Created on Mon Apr  7 14:22:19 2014

@author: thierry
"""

import network_features as nf

class Firewall():
    """@brief Firewall definition and features
    
    @param name 
    @param manufacturer
    @param osversion
    @param hostname
    """

    def __init__(self, name = None, manufacturer = None, osversion = None, hostname = None):
        self.name = name
        self.manufacturer = manufacturer
        self.osversion = osversion
        self.hostname = hostname
        
        self.interfaces = nf.InterfaceList()
        self.acl_table = nf.ACLtable()
        
        self.routes = nf.RouteList()
        
    def __str__(self):
        """
        Print the caracteristics of the firewall
        """
        # General caracteristics
        print "Firewall name : " + str(self.name)
        print "Manufacturer : " + str(self.manufacturer)
        print "OS version : " + str(self.osversion)
        print "Hostname : " + str(self.hostname)

        return ""

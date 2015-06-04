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
Created on Fri Aug  1 15:24:25 2014

@author: thierry
"""

class Switchport():
    """@brief Switchport definition and features
    
    @param interface : interface name
    @param active : True or False
    @param description
    @param vlan : number of the VLAN, native VLAN if mode trunk for Cisco
    @param mode : trunk, access, ...
    
    """

    def __init__(self):
        self.interface = ''
        self.active = ''
        self.description = ''
        self.vlan = ''
        self.vlan_allowed = []
        self.mode = ''
        
    def __str__(self):
        """
        Print the caracteristics of the Switchport
        """
        # General caracteristics
            
        return "%s%s%s%s%s%s" %((str(self.interface)).ljust(30),\
            (str(self.active)).ljust(10), (str(self.vlan)).ljust(10), (str(self.vlan_allowed)[1:-1]).ljust(35), (str(self.mode)).ljust(20), (str(self.description)).ljust(30))

        return ""

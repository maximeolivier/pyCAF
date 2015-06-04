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
Created on Fri Aug  1 15:11:22 2014

@author: thierry
"""

class Interface():
    """@brief Interface definition and features
    
    @param interface : exact interface name (ex : GigabitEthernet0/1.203)
    @param name
    @param active : True or False
    @param ip
    @param mask
    @param urpf : True of False for unicast reverse port forwarding
    @param acl_list_in : Name of the ACL list IN
    @param acl_list_out : Name of the ACL list OUT
    
    """

    def __init__(self):
        self.name = ''
        self.active = ''
        self.ip = ''
        self.mask = ''
        self.urpf = ''
        self.acl_list_in = ''
        self.acl_list_out = ''
        self.description = ''
        
    def __str__(self):
        """
        Print the caracteristics of the Interface
        """
        # General caracteristics
            
        return "%s%s%s%s%s%s%s" %((str(self.name)).ljust(30),\
            (str(self.active)).ljust(10), (str(self.ip)).ljust(18), (str(self.mask)).ljust(18), (str(self.urpf)).ljust(10),\
            (str(self.acl_list_in)).ljust(20), (str(self.acl_list_out)).ljust(20))

        return ""

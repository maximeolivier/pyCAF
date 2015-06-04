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
Created on Fri Aug  1 14:39:30 2014

@author: thierry
"""

class ACL():
    """@brief ACL definition and features
    
    @param type : integer idle(0), standard(1) or extended(2)
    @param filter : permit, deny 
    @param protocol : tcp, udp,...
    @param comment : explication about the ACL
    @param host : True or False (if True, exact IP address and no mask)
    @param src_ip : IP source
    @param src_port : port source
    @param src_mask : mask source if it is not a host
    @param dst_ip : IP destination
    @param dst_port : port destination
    @param dst_mask : mask destination if it is not a host
    @param active : True or False
    
    """

    def __init__(self):
        self.type = 0
        self.filter = ''
        self.protocol = ''
        self.comment = ''
        self.host = ''
        self.src_ip = ''
        self.src_port = ''
        self.src_mask = ''
        self.dst_ip = ''
        self.dst_port = ''
        self.dst_mask = ''
        self.active = ''
        
    def __str__(self):
        """
        Print the caracteristics of the ACL
        """
        # General caracteristics
        if self.type == 1:
            type_acl = "standard"
        elif self.type == 2:
            type_acl = "extended"
        else :
            type_acl = "idle"
            
        return "%s%s%s%s%s%s%s%s%s%s%s" %(type_acl.ljust(10), (str(self.filter)).ljust(10),\
            (str(self.protocol)).ljust(12), (str(self.src_ip)).ljust(18), (str(self.src_mask)).ljust(18), (str(self.src_port)).ljust(18),\
            (str(self.dst_ip)).ljust(18), (str(self.dst_mask)).ljust(18), (str(self.dst_port)).ljust(18), (str(self.active)).ljust(6),\
            (str(self.comment)).ljust(30))

        return ""

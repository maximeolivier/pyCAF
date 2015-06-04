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

class Interface():
    """Definition of what is an Interface
    
    @param name : Name interface (eth0, lo,..)
    @param mac : MAC adress oth the intreface
    @param ip_adress : Ip adress of the interface
    @param mask : Network mask
    @param ipv6_adress : IP v6 address of the interface
    """
    
    def __init__(self, name = None, mac = None, ip_adress = None, mask = None, ipv6_address = None):
        self.name = name
        self.mac = mac
        self.ip_adress = ip_adress
        self.mask = mask
        self.ipv6_address = ipv6_address

    def __str__(self):
        return "%s%s%s%s%s" %(str(self.name).ljust(50), str(self.ip_adress).ljust(18), str(self.mask).ljust(18),\
        str(self.mac).ljust(20), str(self.ipv6_address).ljust(40))
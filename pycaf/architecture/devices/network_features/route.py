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
#Created on Mon Aug  4 17:00:22 2014
#
#@author: thierry
#"""

class Route():
    """@brief Route definition and features
    
    @param destination : ip address of the destination
    @param mask
    @param interface : ip address of the interface
    
    """

    def __init__(self):
        self.destination = ''
        self.mask = ''
        self.interface = ''
        
    def __str__(self):
        """
        Print the caracteristics of the route
        """
        # General caracteristics
            
        return "%s%s%s" %((str(self.destination)).ljust(20), (str(self.mask)).ljust(20), (str(self.interface)).ljust(20))

        return ""

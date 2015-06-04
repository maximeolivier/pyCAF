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
Created on Mon Aug  4 10:38:25 2014

@author: thierry
"""

class Vlan():
    """@brief vlan definition and features
    
    @param name : vlan name
    @param number
    
    """

    def __init__(self):
        self.name = None
        self.number = None
        
    def __str__(self):
        """
        Print the caracteristics of the VLAN
        """
        # General caracteristics
            
        return "%s%s" %((str(self.number)).ljust(8), (str(self.name)).ljust(40))

        return ""

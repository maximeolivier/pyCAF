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
Created on Mon Jul  7 09:25:13 2014

@author: thierry
"""

class GroupWindows():
    """
    Definition of a Group at windows serever
    
    @param group
    @param group_type
    @param group_member
    @param member_type
    @param comment
    """

    def __init__(self, group = None, group_type = None, group_member = None, member_type = None, comment = None):
        self.group = group
        self.group_type = group_type
        self.group_member = group_member
        self.member_type = member_type
        self.comment = comment

    def __str__(self):
        """
        Print windows group attributes
        """
        return "%s%s%s%s%s" %(self.group.ljust(20), self.group_type.ljust(25), self.group_member.ljust(40), self.member_type.ljust(20), self.comment.ljust(20))
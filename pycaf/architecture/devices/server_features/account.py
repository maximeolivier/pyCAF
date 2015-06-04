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

class Account():
    """Definition of what is an Account
    
    @param uid : Unique IDentifier of the account
    @param name : Name of the account
    @param group_id : group ID
    @param group_name : the name of the group
    """

    def __init__(self, uid, name, group_id=None, group_name=None):
        self.uid = uid
        self.name = name
        self.group_id = group_id
        self.group_name = group_name
    
    def __str__(self):
        """
        Print account attributes
        """
        return "%s%s%s%s" % (self.uid.ljust(20), self.name.ljust(20), self.group_id.ljust(20), self.group_name.ljust(20))
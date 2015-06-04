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
Created on Tue May 20 15:01:43 2014

@author: thierry
Class file
"""

class File():
    """Definition of what is a file
    
    @param path : full path of the file
    @param rights : a 10 char string wich contain nature and rights (-rwxrwxrwx)
    @param user : file owner
    @param group : file group owner
    @param time : the date of last modification
    """

    def __init__(self, path, rights, user, group, time):
        self.path = path
        self.rights = rights
        self.user = user
        self.group = group
        self.time = time
    
    def __str__(self):
        """
        Print file attributes
        """
        return "%s%s%s%s%s" % (str(self.rights).ljust(15), str(self.user).ljust(20),
                               str(self.group).ljust(20), str(self.time).ljust(16), (str(self.path)).ljust(60))
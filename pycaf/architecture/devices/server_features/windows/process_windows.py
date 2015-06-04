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

class ProcessWindows():
    """
    Definition of a Process
    
    @param pid : processus ID
    @param name : process name
    @param username : user who have launched the process
    @param session : The session name where the process is running.
    """

    def __init__(self, pid=None, name=None, username=None, session=None):
        self.pid = pid
        self.name = name
        self.username = username
        self.session = session

    def __str__(self):
        """
        Print windows process attributes
        """
        return "%s%s%s%s" %(self.pid.ljust(6), self.name.ljust(25), self.username.ljust(40), self.session.ljust(20))
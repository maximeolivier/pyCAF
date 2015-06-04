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
Created on Mon Jul  7 10:21:02 2014

@author: thierry
"""

class ServiceWindows():
    """Definition of what is a Windows service
     
     @param name : full name of the service
     @param status : current status of the service (running, stopped, etc)    
     @param type : if gave, type like Win32, Kernel, etc
     @param account : owner account of the service
    """
    def __init__(self, name, status, service_type, account):
        self.name = name
        self.status = status
        self.service_type = service_type
        self.account = account
        
    
    def __str__(self):
        """
        Print service attributes
        """
        return "%s%s%s%s" %(str(self.name).ljust(30), str(self.status).ljust(15), str(self.service_type).ljust(15), str(self.account).ljust(25))
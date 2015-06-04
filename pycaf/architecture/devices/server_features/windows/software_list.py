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
Created on Mon Jul  7 11:45:56 2014

@author: thierry
"""

class SoftwareWindowsList():
    
    """
    Class wich create a list of software installed on a Windows server.
    """

    def __init__(self):
        self.dict = {}
        self.counter=0

    def add_software(self, soft):
        """
        Add a process at the server dictionnary
        Dictionnary model : [counter,process]
        @param process : the process to store
        """
        self.counter += 1
        self.dict[self.counter] = soft
        
    def get_software(self,ident):
        """
        Return a process corresponding to the ident value
        @param ident : the number corresponding to the process
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "software not found"
        
            
    def label_software_list(self):
        return "\n%s\n" %("Software installed :".ljust(50))

    def __str__(self):
        """
        Print the list of software with their ident number.
        """
        print self.label_software_list()
        
        for identityNb, soft in self.dict.items():
            print "%s"%(str(soft).ljust(90)),
            print identityNb
        return ""
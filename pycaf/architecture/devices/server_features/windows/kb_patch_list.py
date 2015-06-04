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
Created on Mon Jul  7 09:50:39 2014

@author: thierry
"""


class KBpatchList():
    """
    Class wich create a list of KB patches
    """

    def __init__(self):
        self.dict = {}
        self.counter=0

    def add_kb(self, kb_patch):
        """
        Add a KB patch at the server dictionnary
        Dictionnary model : [counter,kb_patch]
        """
        self.counter += 1
        self.dict[self.counter] = kb_patch
        
    def get_kb(self,ident):
        """
        Return a KB patch corresponding to the ident value
        @param ident : the number corresponding to the interface
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "KB not found"
            
    def push_kb_list(self,listToPush):
        """
        Push a list[] containings KB in the self.kb_patches object
        """
        import datetime
        # Sort the list in date order
        listToPush = sorted(listToPush, key=lambda kb_uptodate: datetime.datetime.strptime(kb_uptodate.date, '%d/%m/%Y'), reverse = True)
        for kb in listToPush:
            self.add_kb(kb)

    def label_kb_list(self):
        return "\n%s%s%s%s\n" %("KB ID".ljust(10), "Date".ljust(15), "Rating".ljust(12), "Description".ljust(120))
    
    def __str__(self):
        """
        Print the list of interfaces with their ident
        """
        print self.label_kb_list()
        
        for identityNb, kb_patch in self.dict.items():
            print "{}".format(kb_patch),
            print identityNb
        return ""

        
        
        
        
        
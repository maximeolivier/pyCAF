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
Created on Mon Jul  7 09:40:32 2014

@author: thierry
"""

class KBpatch():
    """Definition of what is a KB patch (Knowledge base)
     
     @param id : (Unique) ID of the KB
     @param date : Date of the patch    
     @param description : Short description of what is the content.
    """
    def __init__(self, kb_id, date = None, description = None, rate = None):
        self.id = kb_id
        self.date = date
        self.description = description
        self.rate = rate
        
    
    def __str__(self):
        """
        Print KB attributes
        """
        if self.date is not None and self.description is not None:
            return "%s%s%s%s" %(str(self.id).ljust(10), str(self.date).ljust(15), str(self.rate).ljust(12), str(self.description).ljust(120))
        else:
            return "%s" %(str(self.id).ljust(75))
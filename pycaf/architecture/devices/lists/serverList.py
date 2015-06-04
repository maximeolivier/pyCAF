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


class ServerList():
    """
    Class wich create a list of server
    This class uses a dictionnary and a ident number is given at each server added.
    User can get a server with printing the list and pick up the ident value.
    
    Example :
    >>print myServerList
    ServerAlpha         Id : 1
    ServerBeta          Id : 2
    
    >>s = myServerList.get_server(2)
    >>print s.name
    ServerBeta
    """

    def __init__(self):
        self.dict = {}
        self.counter=0
        

    def add_server(self, server):
        """
        Add a server at the server dictionnary
        Dictionnary model : [counter,server]
        @param server : the server to store
        """
        self.counter += 1
        self.dict[self.counter]=server
        
        
    def get_server(self, ident):
        """
        Return a server corresponding to the ident value
        @param ident : the number corresponding to the server
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "Server not found"


    def __str__(self):
        """
        Print the list of server with their ident value
        """
#        print self.label_interface_list()
        
        for identityNb, server in self.dict.items():
            print "{}".format(server),
            print identityNb
        return ""
    
        

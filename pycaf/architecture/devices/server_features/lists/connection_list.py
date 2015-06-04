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
import pycaf.tools as tools

class ConnectionList():
    """Definition of what a ConnectionList is

    A connections list is an object use for manage multiple connections into a server
    This class uses a dictionnary and a ident number is given at each connection added.
    User can get a connection with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_connection(self, connection):
        """
        Add a connection at the server dictionnary
        Dictionnary model : [counter,connection]
        @param connection : the connection to store
        """
        self.counter += 1
        self.dict[self.counter]=connection
        
    def get_connection(self,ident):
        """
        Return a connection corresponding to the ident value
        @param ident : the number corresponding to the connection
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "connection not found"
            
    def filter_connections(self,*args, **kwargs):
        """
        Filter all connections if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return connections with identification numbers : 
            filter_connections(4,6,8,...)
            
        Return connections with specific values :
            filter_connections(keyword="arg", keword2="arg2",....)
        keywords available :
        - protocol
        - src_ip
        - src_port
        - dst_ip
        - dst_port
        - state
        - pid
        - program
        example : filter_connections(protocol="tcp", state="ESTABLISHED")
        """
        list_filtered = ConnectionList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_connection(elem)

        return list_filtered
            
    def show_connections(self,*args, **kwargs):
        """
        Display all connections if any arguments or apply filter with this standard

        No arguments : display all        
        
        Print connections with identification numbers : 
            show_connections(4,6,8,...)
            
        Filter connections with specific values :
            show_conections(keyword="arg", keword2="arg2",....)
        keywords availables :
        - protocol
        - src_ip
        - src_port
        - dst_ip
        - dst_port
        - state
        - pid
        - program
        keywords availables for black list:
        - hide_protocol
        - hide_src_ip
        - hide_src_port
        - hide_dst_ip
        - hide_dst_port
        - hide_state
        - hide_pid
        - hide_program
        example : show_conections(protocol="tcp", state="ESTABLISHED")
        """
        list_filtered = self.filter_connections(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered
            
                    
    def label_connection_list(self):
        return "\n%s%s%s%s%s%s%s%s%s%s\n" %("protocol".ljust(10), "src_ip".ljust(18), "src_port".ljust(10),\
        "dst_ip".ljust(18), "dst_port".ljust(10), "state".ljust(15), "pid".ljust(10), "program".ljust(20),\
        "src_hostname".ljust(15), "dst_hostname".ljust(15))

    def __str__(self):
        """
        Print the list of connections with their ident
        """
        print self.label_connection_list()
        
        for identityNb, connection in self.dict.items():
            print "{}".format(connection),
            print identityNb
        return ""

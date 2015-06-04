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

class Connection():
    """Definition of what is a Connection
     
     @param protocol : Protocol used by the connection
     @param src_ip : IP source
     @param src_port : Source port
     @param dst_ip : IP destination
     @param dst_port : Destination port
     @param state : Current state of the connection (listen, established, ...)
     @param pid : pid of the process wich manage the connection
     @param program : name of the program corresponding to the pid
    """
    def __init__(self, protocol, src_ip, src_port, dst_ip, dst_port, state, pid = None, program = None):
        self.protocol = protocol
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.state = state
        self.pid = pid
        self.program = program
        self.src_hostname = ""
        self.dst_hostname = ""
        
    
    def __str__(self):
        """
        Print connection attributes
        """
        return "%s%s%s%s%s%s%s%s%s%s" %(str(self.protocol).ljust(10), str(self.src_ip).ljust(18), str(self.src_port).ljust(10),\
        str(self.dst_ip).ljust(18), str(self.dst_port).ljust(10), str(self.state).ljust(15), str(self.pid).ljust(10), str(self.program).ljust(20), str(self.src_hostname).ljust(15), str(self.dst_hostname).ljust(15))
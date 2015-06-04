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


class Process():
    """
    Definition of a Process
    
    @param pid : processus ID
    @param ppid : parent pid
    @param user : the user wich manage the processus
    @param command : The command which launched the processus
    """

    def __init__(self, pid=None, ppid=None, user=None, command=None):
        self.pid = pid
        self.ppid = ppid
        self.user = user
        self.command = command
        
    def show_full_command(self):
        print "%s%s%s%s" %(self.pid.ljust(6), self.ppid.ljust(6), self.user.ljust(20), self.command.ljust(70))

    def __str__(self):
        """
        Print process attributes
        """
        short_command = self.command.split(' ')
        return "%s%s%s%s" %(self.pid.ljust(6), self.ppid.ljust(6), self.user.ljust(20), short_command[0].ljust(70))

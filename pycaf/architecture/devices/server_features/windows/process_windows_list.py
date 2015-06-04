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
Created on Mon Jul  7 09:35:17 2014

@author: thierry
"""
import pycaf.tools as tools

class ProcessWindowsList():
    
    """
    Class wich create a list of processes
    Definition of what an processList is
    An process list is an object use for manage multiple processes into a server
    This class uses a dictionnary and a ident number is given at each process added.
    User can get a process with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter=0

    def add_process(self, process):
        """
        Add a process at the server dictionnary
        Dictionnary model : [counter,process]
        @param process : the process to store
        """
        self.counter += 1
        self.dict[self.counter]=process
        
    def get_process(self,ident):
        """
        Return a process corresponding to the ident value
        @param ident : the number corresponding to the process
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "process not found"
            
    def filter_processes(self,*args, **kwargs):
        """
        Filter all processes if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return processes with identification numbers : 
            filter_processes(4,6,8,...)
            
        Return processes with specific values :
            filter_groups(keyword="arg", keword2="arg2",....)
        keywords available :
        - pid
        - name
        - username
        - session
        
        example : filter_processes(session="services", username="NT AUTHORITY\SYSTEM")
        
        keywords availables for black list:
        - hide_pid
        - hide_name
        - hide_username
        - hide_session
        example : filter_processes(hide_session="services", username="NT AUTHORITY\SYSTEM")
        """

        list_filtered = ProcessWindowsList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_process(elem)

        return list_filtered
            
    def show_processes(self,*args, **kwargs):
        """
        Display all processes if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return processes with identification numbers : 
            filter_processes(4,6,8,...)
            
        Return processes with specific values :
            filter_processes(keyword="arg", keword2="arg2",....)
        keywords available :
        - pid
        - name
        - username
        - session
        
        example : filter_processes(session="services", username="NT AUTHORITY\SYSTEM")
        
        keywords availables for black list:
        - hide_pid
        - hide_name
        - hide_username
        - hide_session
        example : filter_processes(hide_session="services", username="NT AUTHORITY\SYSTEM")
        """
        list_filtered = self.filter_processes(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered
        
            
    def label_process_list(self):
        return "\n%s%s%s%s\n" %("PID".ljust(6), "Name".ljust(25), "Username".ljust(40), "Session name".ljust(20))

    def __str__(self):
        """
        Print the list of processs with their ident number.
        """
        print "Short command is showed. Refer to the help of this function"
        print self.label_process_list()
        
        for identityNb, process in self.dict.items():
            print "{}".format(process),
            print identityNb
        return ""

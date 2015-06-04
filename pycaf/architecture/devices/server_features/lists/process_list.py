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

class ProcessList():
    
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
            
    def filter_process(self,*args, **kwargs):
        """
        Filter all processes if any arguments or apply filter with this standard
        
        No arguments : no filtering       
        
        Filter processes with identification numbers : 
        filter_process(4,6,8,42,...)
        
        Filter process with specific values :
        filter_process(keyword="arg", keword2="arg2",....)
        keywords available :
        - pid
        - ppid
        - user
        - command
        example : filter_process(user ="root", ppid="2")
        
        Black list some users
        keyword :
        - hide_user
        - hide_pid
        - hide_ppid
        - hide_command
        example 1 : filter_process(hide_user="root")
        example 2 : filter_process(hide_user="root, nobody")
        """
        list_filtered = ProcessList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_process(elem)

        return list_filtered
            
    def show_process(self,*args, **kwargs):
        """
        Display all processes if any arguments or apply filter with this standard

        No arguments : display all        
        
        Print processes with identification numbers : 
            show_connecshow_processions(4,6,8,42,...)
            
        Filter processes with specific values :
            show_process(keyword="arg", keword2="arg2",....)
        keywords available :
        - pid
        - ppid
        - user
        - command
        example : show_process(user ="root", ppid="2")
        
        Black list some users
        keyword :
        - hide_user
        - hide_pid
        - hide_ppid
        - hide_command
        example 1 : show_process(hide_user="root")
        example 2 : show_process(hide_user="root, nobody")
        """
        list_filtered = self.filter_process(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered

        
#    def show_tree(self,pid):
#        """
#        To do
#        """
#        self.filter_process(pid=str())
        
            
    def label_process_list(self):
        return "\n%s%s%s%s\n" %("pid".ljust(6), "ppid".ljust(6), "user".ljust(20), "command (short)".ljust(70))

    def __str__(self):
        """
        Print the list of processs with their ident number.
        Just the short command is showed for a more readable result. It is
        possible to see the full command with this procedure :
        the_process = XXX.processes.get_process(42)
        the_process.show_full_command()
        """
        print "Short command is showed. Refer to the help of this function"
        print self.label_process_list()
        
        for identityNb, process in self.dict.items():
            print "{}".format(process),
            print identityNb
        return ""

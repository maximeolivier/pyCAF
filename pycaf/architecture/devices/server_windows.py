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

import server_features.windows as sw

class ServerWindows():
    """
    Windows Server definition and features
    Specific windows server class.
    """

    def __init__(self, servername=None):
#        self.version_script = None        
        
        self.name = servername
        self.ostype = None
        self.osname = None
        self.osversion = None
        self.osarchitecture = None
        self.kernel_version = None
        
        self.processes = None
        self.connections = None
        self.interfaces = None
        self.services = None
        self.kb_patches = None
        self.software = None
        self.groups = None
        
        # Dictionnary which contain the program name corresponding to the PID
        self.pid_name_dict = {}
        
        # Register the path for the register_raw_info_in_files funtion
        self.registering_path = None
        
        # KB analysis results to save
        self.nb_kb = -1
        self.nb_kb_uptodate = -1
        self.nb_kb_obsolete = -1
        self.nb_kb_not_installed = -1
        self.kb_uptodate = sw.KBpatchList()
        self.kb_obsolete = sw.KBpatchList()
        self.kb_not_installed = sw.KBpatchList()
        
        # IP-hostname dictionnaries
        self.ip_hostname_local = {}
        # Common dictionnay when several servers are imported
        self.ip_hostname_common = {}
        
    def register_raw_info_in_files(self, path = None):
        """
        Function wich save all raw imported information in several files
        Put the path as argument or take the logs_path in pycaf.conf
        """
        import os
        import sys        
        
        if path is None and self.registering_path is None:
            print "No path specified, please put a valid path"
            return False
        else:
            if path is None:
                path = self.registering_path
            if not os.path.exists(path):
                print "Path specified is wrong, enter a valid path (ex : /tmp/)"
                return False
            else:
                if path[-1] != "/":
                    path += "/"
                    
                folder_name = str(self.name) + "_raw_info"
                path_to_register = str(path) + folder_name
                if not os.path.exists(path_to_register):
                    os.makedirs(path_to_register)

                list_to_register = ['connections', 'interfaces', 'processes', 'services', 'kb_patches', 'software', 'groups']
                for param_to_save in list_to_register:
                    file_name = self.name + "_raw_info_" + str(param_to_save) + ".txt"
                    path_file = path_to_register + "/" + file_name
                    file_param = open(path_file, 'wb')
                    
                    orig_stdout = sys.stdout
                    sys.stdout = file_param
                    
                    print self
                    print getattr(self,param_to_save)
                    
                    sys.stdout = orig_stdout
                    file_param.close()
                    
                return True
                
            
            

    def __str__(self):
        """
        Print the caracteristics and summary results
        """
        # General caracteristics
        print "\nServer name : " + str(self.name)
        print "OS name : " + str(self.osname)
        print "OS architecture : " + str(self.osarchitecture)
        print "OS version : " + str(self.osversion)
        print "Kernel version : " + str(self.kernel_version)
            
        return ""

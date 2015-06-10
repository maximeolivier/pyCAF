# -*- coding: utf-8 -*-

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


import server_features as sf

class Server():
    """@brief Server definition and features
    
    @param servername The server name given bu user
    @param ostype The OS family (Unix, Linux, Windows, BSD, Solaris, ...)
    @param osname The exact OS name 
    @param osversion Kernel OS version
    @param accountsList TO DO
    """

    def __init__(self, servername=None, ostype=None, osname=None, osversion=None, osarchitecture = None, kernel_release = None, kernel_version_running = None, accountslist=None,\
    processeslist=None, connectionslist=None, interfaceslist=None, packageslist=None, version_script=None):
        """ Objet serveur
        """
        self.name = servername
        self.ostype = ostype
        self.osname = osname
        self.osversion = osversion
        self.osarchitecture = osarchitecture
        self.kernel_release = kernel_release
        self.kernel_version_running = kernel_version_running

        self.accounts = accountslist
        self.processes = processeslist
        self.connections = connectionslist
        self.interfaces = interfaceslist
        self.packages = packageslist
        self.version_script = version_script

        # Packages analysis
        self.nb_packages = -1
        self.nb_packages_uptodate = -1
        self.nb_packages_obsolete = -1
        self.nb_packages_unchecked = -1
        self.packages_uptodate = sf.PackageList()
        self.packages_obsolete = sf.PackageList()
        self.packages_unchecked = sf.PackageList()

        self.kernel_version_installed = None
        self.kernel_version_uptodate = None
        # Kernel can have 4 states :
        # 1 : Critical state : the release is obsolete
        # 2 : Warning state : the version of the kernel is obsolete (just update package)
        # 3 : Warning state 2 : the right version is installed but not running. Need to reboot the PC.
        # 4 : Clear state : the kernel release and version are up to date
        self.kernel_result = -1

        # Analyze processes
        # Listening and established connections
        self.listening_connections = sf.ConnectionList()
        # Process whose user is Root
        self.root_processes = sf.ProcessList()
        # Listening connection whose user is root
        self.listening_root_process = sf.ProcessList()

        # Files lists
        self.files = sf.FileList()
        self.files_potentially_threat = sf.FileList()

        # PAM conf (string contains utility configuration)
        self.pam = ""

        # nsswictch conf (string contains utility configuration)
        self.nsswitch = ""

        # SSH config object (see server features objects)
        self.ssh_config = sf.SSHConfig()
        
        # Suoders config
        self.sudoers_config = ""

        # fstab config
        self.fstab_config = ""

        # crontab config dictionnary
        #{"USER","crontab rules1 \nrules2 \nrules3"}
        self.crontab_config = {}
        self.crontab_rules_counter = 0
        # Crontab files analysis results. [[user,file_path,ok], [user,file_path,ko], [user,file_path,ok], ...]
        self.crontab_results = []

        # IP-hostname dictionnaries
        self.ip_hostname_local = {}
        # Common dictionnay when several servers are imported
        self.ip_hostname_common = {}

    def set_name(self, name):
        """ Setter pour la propriété name d'un serveur
        """
        self.name = name

    def set_ostype(self, ostype):
        """ Setter pour la propriété ostype d'un serveur
        """
        self.ostype = ostype

    def set_osname(self, osname):
        """ Setter pour la propriété osname d'un serveur
        """
        self.osname = osname

    def set_osversion(self, osversion):
        """ Setter pour la propriété osversion d'un serveur
        """
        self.osversion = osversion

    def set_osarchitecture(self, osarchitecture):
        """ Setter pour la propriété osarchitecture d'un serveur
        """
        self.osarchitecture = osarchitecture

    def set_kernel_release(self, kernel_release):
        """ Setter pour la propriété kernel_release d'un serveur
        """
        self.kernel_release = kernel_release

    def set_kernel_version_running(self, kernel_version_running):
        """ Setter pour la propriété kernel_version_running d'un serveur
        """
        self.kernel_version_running = kernel_version_running
        
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

                list_to_register = ['accounts', 'connections', 'interfaces', 'processes', 'packages', 'files', 'pam', 'nsswitch', 'ssh_config', 'sudoers_config', 'fstab_config', 'crontab_config']
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
        print "OS version : " + str(self.osversion)
        print "OS architecture : " + str(self.osarchitecture)
        print "Kernel release : " + str(self.kernel_release)
        print "Kernel version running : " +str(self.kernel_version_running)
        
        if self.kernel_version_installed is not None:
            print "Kernel version installed : " +str(self.kernel_version_installed)
        if self.kernel_version_uptodate is not None:
            print "Kernel version up to date : " +str(self.kernel_version_uptodate)
            
        return ""

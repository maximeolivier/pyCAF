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
Analyze the kernel release and version
"""
import threading
import time
import gzip
import os
import sys
import re

# We need to have thread locker to download or access the package downloads
# This analyzer is very close to analyze_packages.py


# Need to set the path at root project directory if necessary (doctest)
if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):    
    PROJECT_PATH = os.path.dirname(os.path.abspath('../..'))
    sys.path.append(PROJECT_PATH)

import pycaf.tools as tools
import pycaf.architecture.devices.server_features as sf
import pycaf.architecture.devices as dvc
import ressources.analyzer.server as ressources
        
class AnalyzeDebianKernel (threading.Thread):
    """Download on the internet packages corresponding to the distribution and 
    check the kernel version
    
    >>> config = tools.ConfigParse()
    >>> lock = threading.Lock()
    >>> srv = dvc.Server()
    >>> srv.osname = "wheezy"
    >>> srv.kernel_release = "3.2.0-4-amd64"
    >>> srv.kernel_version = "3.2.54-2"
    >>> thd = AnalyzeDebianKernel(srv, config, lock)
    >>> thd.analyze()
    True
    >>> thd.check_results()
    True
    >>> thd.send_results()
    
    """
        
    def __init__(self, server, config, lock): 
        threading.Thread.__init__(self)
        self.server = server
        self.config = config
        self._logger = tools.create_logger(__name__, self.config)
        self.config_server = ressources.ConfigServer(1)
        
        self._lock = lock
    
    def run(self):
        self._logger.info("Run Analyze Debian Kernel")
        if self.check_ressources():
            self.analyze()
            if self.check_results():
                self.log_results()
                return True
            else:
                self._logger.error("AnalyzeDebianPackages Error")
                return False
        else:
            self._logger.error("AnalyzeDebianPackages Error")
            return False
                    
    def analyze(self):
        """
        Core function which is called in the run
        Do the effective work
        """
        start_time = time.time()
        
        path = self.config.ressources_path
        
        if path is None:
            path = "/tmp/"
        
        # Create the directory containig data if it does not exist
        if not os.path.exists(path):
            os.makedirs(path)
        
        # We now we are in a debian distribution
        # Debian packages are available at this site :
        # https://packages.debian.org/fr/X/allpackages?format=txt.gz
        debian_version = self.server.osname
        #Check if realase packages are ever stored
        #Check if the realease packages are the last version
        #Download the last realease packages of the well distribution (Lenny, wheezy,...)
            
        # Check if other packages lists availables (updates, backports,...)
        analyze_distrib_list = []
        # Get stable debian version list
        debian_list = self.config_server.debian["stable_versions"]

        # Filter specific distribution (exemple : wheezy) 
        for distrib in debian_list:
            if debian_version in distrib:
                analyze_distrib_list.append(distrib)
        # Reorganyze the list in order to start by backports, then updates and finaly base.
        # Sort the list : [distrib, distrib_backports, distrib_updates]
        analyze_distrib_list.sort()
        # Rotate the list of -1 to put the first at the end : [distrib_backports, distrib_updates, distrib]
        analyze_distrib_list = analyze_distrib_list[1:] + analyze_distrib_list[:1]
    
        distribution = analyze_distrib_list[-1]
        self._logger.info("Debian"+str(distribution)+\
        " kernel analysis in progress...")
            
        # Download packages list if necessary 
        url = self.config_server.debian["packages_url"].replace("DISTRIBUTION", str(distribution))
        file_name = distribution + "_packages.gz"

        # Add a lock to prevent conflict access with the analyze package function            
        self._lock.acquire()
        download_boolean = tools.downloadFile(url, file_name, self.config, path)
        self._lock.release()
        if not download_boolean :
            self._logger.error("Download file error")
            return False
  
        # Read the file containing packages list
        self._lock.acquire()
        file_path = path + file_name
        f_1 = gzip.open(file_path,'rb')
        rawtext = f_1.read()
        f_1.close()
        self._lock.release()
        
        # Split text in lines
        releases = rawtext.split('\n')
        
        # Dictionnary of release kernel    
        pkg_release_expression = r"(?P<var1>^[A-Za-z0-9:\-~.+]+)(?P<var2> \()(?P<var3>[A-Za-z0-9:\-~.+]+)(?P<var4>[ \)]{1})"  
        pkg_release_reg = re.compile(pkg_release_expression)
        
        # List which contain the kernel package(s)
        kernel_pkg_dwnld = None
        
        # Regular expression to extract release package name and version
        for l_1 in releases:
            if pkg_release_reg.match(l_1) is not None:
                result_re = pkg_release_reg.match(l_1)
                pkg_name = result_re.group('var1')
                pkg_version = result_re.group('var3')
                
                if pkg_name == "linux-image-" + str(self.server.kernel_release) and "dummy package" not in l_1:
                    if kernel_pkg_dwnld is not None:
                        self._logger.error("Several pacakges corresponding to the release kernel version")
                        return False
                    else:
                        kernel_pkg_dwnld = sf.Package(pkg_name, pkg_version)
                        self.server.kernel_version_uptodate = pkg_version

        # Check kernel algorithm
        # Step 1 : check RELEASE from "uname.txt" with the downloaded package list
        # Ok -> next step    KO -> Critical obsolescence
        # Step 2 : check VERSION from "uname.txt" with the downloaded package list
        # Ok -> uptodate    KO -> next step
        # Step 3 : check VERSION of the host list (dpkg.txt) with the downloaded package list
        # Ok -> Uptodate but need reboot    KO -> Obsolete version (and good release)


        # --------------------------------------------
        # ------------------ Step 1 ------------------
        # --------------------------------------------
        # If release_kernel_list is empty, linux-image-"kernelRelease" not found and obsolete
        if kernel_pkg_dwnld is None:
             self.server.kernel_result = 1
        
        # --------------------------------------------
        # ------------------ Step 2 ------------------
        # --------------------------------------------
        else:
            if self.server.kernel_version_running == kernel_pkg_dwnld.version:
                # Kernel up to date
                self.server.kernel_result = 4
            
            # --------------------------------------------
            # ------------------ Step 3 ------------------
            # --------------------------------------------
            else:
                if self.server.kernel_version_installed == kernel_pkg_dwnld.version:
                    self.server.kernel_result = 3
                else:
                    self.server.kernel_result = 2
        
        end_time = time.time()
        self._logger.info("Elapsed time: "+str((end_time - start_time) * 1000)+" msecs")                    
        return True
    
    def check_ressources(self):
        """
        Check ressources before processing the analyze
        """
        # Check internet connection
        self._lock.acquire()
        internet_access = tools.checkInternetAccess(self.config)
        self._lock.release()
        
        if self.server.kernel_release is None or self.server.kernel_version_running is None:
            self._logger.error("Test impossible : kernel release or version empty")
        if not internet_access:
            self._logger.error("Test impossible : check your internet access")
            return False
        else:
            self._logger.debug("Ressources checked for Debian package analysis")
            return True
        
        
    
    def check_results(self):
        """
        Check results after analyze in order to detect analysis error
        For example : kernel result = -1
        """
        if self.server.kernel_result == -1:
            self._logger.error("Ckeck results : kernel_results = -1")
            return False
        else:
            return True
        
        
    
    def log_results(self):
        """
        Report formatting in order to show results at user
        Kernel can have 4 states :
        1 : Critical state : the release is obsolete
        2 : Warning state : the version of the kernel is obsolete (just update package)
        3 : Warning state 2 : the right version is installed but not running. Need to reboot the PC.
        4 : Clear state : the kernel release and version are up to date
        """
        self._logger.debug("Debian kernel analyze results")
        self._logger.info("Release : " + str(self.server.kernel_release) + " / version running : " + str(self.server.kernel_version_running)
        + " / version installed : " + str(self.server.kernel_version_installed) + " / version up to date : " + str(self.server.kernel_version_uptodate))
        if self.server.kernel_result == 4:
            self._logger.info("The kernel release and version are up to date.")
            return True
        elif self.server.kernel_result == 3:
            self._logger.warning("The kernel release and version are up to date but the PC need to reboot.")
            return True
        elif self.server.kernel_result == 2:
            self._logger.warning("The kernel release is up to date but the version is obsolete. Proceed updates")
            return True
        elif self.server.kernel_result == 1:
            self._logger.warning("The kernel release is obsolete. Urgent kernel updating !!!")
            return True
        else:
            self._logger.error("Debian kernel analyzer error")
            return False
            
    def print_results(self):
        """
        Print results at user
        Kernel can have 4 states :
        1 : Critical state : the release is obsolete
        2 : Warning state : the version of the kernel is obsolete (just update package)
        3 : Warning state 2 : the right version is installed but not running. Need to reboot the PC.
        4 : Clear state : the kernel release and version are up to date
        """
        print "\n=============================================================================="
        print "==                      Kernel analysis results                             =="
        print "=============================================================================="
        print ("Release : " + str(self.server.kernel_release) + " / version running : " + str(self.server.kernel_version_running)
        + " / version installed : " + str(self.server.kernel_version_installed) + " / version up to date : " + str(self.server.kernel_version_uptodate))
        if self.server.kernel_result == 4:
            print "The kernel release and version are up to date."
        elif self.server.kernel_result == 3:
            print "The kernel release and version are up to date but the PC need to reboot."
        elif self.server.kernel_result == 2:
            print "The kernel release is up to date but the version is obsolete. Proceed updates"
        elif self.server.kernel_result == 1:
            print "The kernel release is obsolete. Urgent kernel updating !!!"
        else:
            print "Debian kernel analyzer error"
        

            
if __name__ == "__main__":
    import doctest
    doctest.testmod()

               

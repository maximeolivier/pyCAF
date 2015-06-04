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



"""
Analyze packages to check updates availables
"""
import threading
import time
import gzip
import os
import sys
import re
import urllib2


# Need to set the path at root project directory if necessary (doctest requirement)
if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):    
    PROJECT_PATH = os.path.dirname(os.path.abspath('../..'))
    sys.path.append(PROJECT_PATH)

import pycaf.tools as tools
import pycaf.architecture.devices.server_features as sf
import pycaf.architecture.devices as dvc

import ressources.analyzer.server as ressources

class AnalyzeCentosPackages (threading.Thread):
    """Download on the internet packages corresponding to the distribution and 
    check the versions
    
    >>> config = tools.ConfigParse()
    >>> lock = threading.Lock()
    >>> srv = dvc.Server()
    >>> srv.osname = "centos"
    >>> srv.packages = sf.PackageList()
    >>> srv.packages.add_package(sf.Package("acpitail", "0.1-4"))
    >>> srv.packages.add_package(sf.Package("invented", "42"))
    >>> srv.packages.add_package(sf.Package("acct", "6.4"))
    >>> thd = AnalyzeCentosPackages(srv, config, lock)
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
        self.packages = server.packages
        self.active = False
        self._logger = tools.create_logger(__name__, self.config)
        self._lock = lock
        self.config_server = ressources.ConfigServer(2)
    
    def run(self):
        self._logger.info("Run Analyze CentOS Packages")
        if self.check_ressources():
            self.analyze()
            if self.check_results():
                self.log_results()
                return True
            else:
                self._logger.error("AnalyzeCentOSPackages Error")
                return False
        else:
            self._logger.error("AnalyzeCentOSPackages Error")
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
        
        # Check packages algorithm
        # Step 1 : check packages in updates packages
        # Ok -> uptodate    KO -> undetermine (uptodate or obsolete or unchecked)
        # Step 2 : check name with updates packages
        # Ok -> obsolete    KO -> undetermine (uptodate or obsolete or unchecked)
        # Step 3 : check packages with centos release
        # Ok -> uptodate    KO -> undetermine (obsolete or unchecked)
        # Step 4 : check name with centos release
        # Ok -> obsolete    KO -> unchecked
        
        # List of package object to analyze
        packages_list_to_analyze = self.packages.dict.values()
        
        # Temporary lists to manage packages
        packages_tmp_uptodate = []
        packages_tmp_obsolete = []
        packages_tmp_unchecked = []
            
        # Download packages list if necessary 
        # "http://mirrors.atosworldline.com/public/centos/filelist.gz"
        url = self.config_server.centos["packages_url_stable_version"]
        print "url : " + url
        file_name = "centos_packages.gz"
        
        pkg_string_header = "./" + self.server.osversion + "/os/" + self.server.osarchitecture + "/CentOS/"
        pkg_string_header_update = "./" + self.server.osversion + "/updates/" + self.server.osarchitecture + "/RPMS/"        
        pkg_release_expression = pkg_string_header + "(?P<pkg_release>[A-Za-z0-9:\-~.+_]+)"
        pkg_update_expression = pkg_string_header_update + "(?P<pkg_update>[A-Za-z0-9:\-~.+_]+)" 
        #pkg_obsolete_expression = "(?P<pkg_name_start>[A-Za-z0-9:+~\-\._]+)(?P<pkg_version>(\-))"
        pkg_obsolete_expression = "(?P<pkg_name_start>[A-Za-z0-9:+~\-\._]+)"
        
        pkg_release_reg = re.compile(pkg_release_expression)
        pkg_update_reg = re.compile(pkg_update_expression)
        pkg_obsolete_reg = re.compile(pkg_obsolete_expression)
        
        # List of release packages
        release_list = []
        # List of updates packages
        updates_list = []
        
        if self.server.osversion in self.config_server.centos["stable_versions"]:
            self._lock.acquire()
            download_boolean = tools.downloadFile(url, file_name, self.config, path)
            self._lock.release()
            if not download_boolean:
                self._logger.error("Download file error")
                return False
                
            # Read the downloaded file containing packages list 
            file_path = path + file_name
            f_1 = gzip.open(file_path,'rb')
            rawtext = f_1.read()
            f_1.close()
            
            # Split text in lines
            releases = rawtext.split('\n')
            
            # Read the lines of packages and fill the release and update pacakges lists
            for l_1 in releases:
                if pkg_release_reg.match(l_1) is not None:
                    # Fill the release list
                    result_re = pkg_release_reg.match(l_1)
                    pkg_name = result_re.group('pkg_release')
                    release_list.append(pkg_name)
                elif pkg_update_reg.match(l_1) is not None:
                    # Fill the updates list
                    result_re = pkg_update_reg.match(l_1)
                    pkg_name = result_re.group('pkg_update')
                    updates_list.append(pkg_name)
        else:
            # url_os = "http://vault.centos.org/" + str(self.server.osversion) + "/os/" + str(self.server.osarchitecture) + "/CentOS/"
            url_os = "http://vault.centos.org/" + str(self.server.osversion) + "/os/SRPMS/"
            url_updates = "http://vault.centos.org/" + str(self.server.osversion) + "/updates/SRPMS/" # + str(self.server.osarchitecture) + "/RPMS/"
            pattern = r"(?P<var1>.*)(?P<var2><a href=\")(?P<pkg>.+)(?P<var3>\.src.rpm\">)"
            
            reg = re.compile(pattern)
            
            lines_os = urllib2.urlopen(url_os).read().split('\n')
            lines_updates = urllib2.urlopen(url_updates).read().split('\n')
            
            for line in lines_os:
                if reg.match(line):
                    result_re = reg.match(line)
                    # release_list.append(result_re.group('pkg') + ".rpm")
                    release_list.append(result_re.group('pkg'))
                    
            for line in lines_updates:
                if reg.match(line):
                    result_re = reg.match(line)
                    # updates_list.append(result_re.group('pkg') + ".rpm")
                    updates_list.append(result_re.group('pkg'))
        # --------------------------------------------
        # ------------------ Step 1 ------------------
        # --------------------------------------------
    
        # tmp_list wich will be the future packages_list_to_analyze after the loop
        tmp_list = []
        for pkg in packages_list_to_analyze:
            # Add the suffix .osarchitecure.rpm
            # ex : package.x86_64.rpm
            pkg_with_arch = pkg.name + "." + self.server.osarchitecture + ".rpm"

            if pkg_with_arch in updates_list or pkg_with_arch.replace(self.server.osarchitecture + ".rpm", "noarch.rpm") in updates_list:
                packages_tmp_uptodate.append(sf.Package(pkg.name, pkg.version))

            else:
                tmp_list.append(pkg)
        packages_list_to_analyze = tmp_list
        
        # --------------------------------------------
        # ------------------ Step 2 ------------------
        # --------------------------------------------
        
        # Dictionnary wich contain the start of the pacakge and the full line
        updates_dict_start={}
        for pkg_update in updates_list:
            if pkg_obsolete_reg.match(pkg_update) is not None:
                result_re = pkg_obsolete_reg.match(pkg_update)
                updates_dict_start[result_re.group('pkg_name_start')] = pkg_update
            else:
                self._logger.error("Regular expression parsing error : step 2 - a")
        
        tmp_list = []
        for pkg in packages_list_to_analyze:
            pkg_found = False    
            if pkg_obsolete_reg.match(pkg.name) is not None:
                result_re = pkg_obsolete_reg.match(pkg.name)
                pkg_name_start = result_re.group('pkg_name_start')
                
                for pkg_update_start in updates_dict_start.keys():
                    if pkg_name_start == pkg_update_start:
                        pkg_found = True
                        packages_tmp_obsolete.append(sf.Package(pkg.name, pkg.version, updates_dict_start[pkg_update_start]))
            else:
                self._logger.error("Regular expression parsing error : step 2 - b")
                
            if not pkg_found:
                tmp_list.append(pkg)

        packages_list_to_analyze = tmp_list
        
        # --------------------------------------------
        # ------------------ Step 3 ------------------
        # --------------------------------------------            
        
        tmp_list = []
        for pkg in packages_list_to_analyze:
            # Add the suffix .osarchitecure.rpm
            # ex : package.x86_64.rpm
            pkg_with_arch = pkg.name + "." + self.server.osarchitecture + ".rpm"

            if pkg_with_arch in release_list or pkg_with_arch.replace(self.server.osarchitecture + ".rpm", "noarch.rpm") in release_list:
                packages_tmp_uptodate.append(sf.Package(pkg.name, pkg.version))

            else:
                tmp_list.append(pkg)
        packages_list_to_analyze = tmp_list
        
        # --------------------------------------------
        # ------------------ Step 4 ------------------
        # --------------------------------------------
        
        release_dict_start={}
        print len(release_list)
        for pkg_release in release_list:
            if pkg_obsolete_reg.match(pkg_release) is not None:
                result_re = pkg_obsolete_reg.match(pkg_release)
                release_dict_start[result_re.group('pkg_name_start')] = pkg_release 
            else:
                self._logger.error("Regular expression parsing error : step 4 - a")
        
        for pkg in packages_list_to_analyze:
            # print "Package  :: " + pkg.name
            pkg_found = False
            if pkg_obsolete_reg.match(pkg.name) is not None:
                result_re = pkg_obsolete_reg.match(pkg.name)
                
                pkg_name_start = result_re.group('pkg_name_start')
                # print "info :: " + pkg_name_start
                if pkg.name == pkg_name_start:
                    pkg_found = True
                    packages_tmp_uptodate.append(sf.Package(pkg.name, pkg.version, ""))
                    print " Package installé : " + pkg.name + "// Package attendu : " + pkg_name_start
                else:
                    print "Package installé : " + pkg.name
                    print "Package attendu  :" + pkg_name_start
                #for pkg_release_start in release_dict_start.keys():
                #    if pkg_name_start == pkg_release_start:
                #        pkg_found = True
                #        packages_tmp_obsolete.append(sf.Package(pkg.name, pkg.version, release_dict_start[pkg_release_start]))
            else:
                self._logger.error("Regular expression parsing error : step 4 - b")
                print "plop"
            if not pkg_found:
                packages_tmp_unchecked.append(sf.Package(pkg.name, pkg.version))

            
#
        # Stored results and sort the list in name alphabetic order 
        self.server.packages_uptodate.push_package_list(packages_tmp_uptodate)
        self.server.packages_obsolete.push_package_list(packages_tmp_obsolete)
        self.server.packages_unchecked.push_package_list(packages_tmp_unchecked)
#    
        # Fill the reporting
        self.server.nb_packages = self.packages.get_number()
        self.server.nb_packages_uptodate = self.server.packages_uptodate.get_number()
        self.server.nb_packages_obsolete = self.server.packages_obsolete.get_number()
        self.server.nb_packages_unchecked = self.server.packages_unchecked.get_number()
        
        self._logger.debug("Nb Packages : "+str(self.server.nb_packages))
        self._logger.debug("Nb up to date : "+str(self.server.nb_packages_uptodate))
        self._logger.debug("Nb Packages obsolete : "+str(self.server.nb_packages_obsolete))
        self._logger.debug("Nb Packages unchecked : "+str(self.server.nb_packages_unchecked) )
    
        
#        
        end_time = time.time()
        self._logger.info("Elapsed time: "+str((end_time - start_time) * 1000)+" msecs")
        self._logger.info("CentOS packages successfully analyzed !")

        
            
        return True
    
    def check_ressources(self):

        """
        Check ressources before processing the analyze
        """
        # Check internet connection
        self._lock.acquire()
        internet_access = tools.checkInternetAccess(self.config)
        self._lock.release()
        if not internet_access:
            self._logger.error("Test impossible : check your internet access")
            return False
        # Check that packages list is not empty    
        elif self.packages.counter == 0:
            self._logger.error("Empty packages list : check your packages list")
            return False
        else:
            self._logger.debug("Ressources checked for CentOS package analysis")
            return True
        
    
    def check_results(self):
        """
        Check results after analyze in order to detect analysis error
        For example : number of packets is to be coherent
        """
        if self.server.nb_packages == 0:
            self._logger.error("Check results : number packages = 0")
            return False
        elif ((self.server.nb_packages_uptodate + self.server.nb_packages_obsolete +self.server.nb_packages_unchecked) != self.server.nb_packages):
            self._logger.warning("Results non coherent")
            self._logger.warning("Nb Packages : "+str(self.server.nb_packages))
            self._logger.warning("Nb up to date : "+str(self.server.nb_packages_uptodate))
            self._logger.warning("Nb Packages obsolete : "+str(self.server.nb_packages_obsolete))
            self._logger.warning("Nb Packages unchecked : "+str(self.server.nb_packages_unchecked) )           
            
            return False
        else:
            self._logger.info("Packages results checked")
            self.server.analyzed_packages = True
            return True
        
        
    
    def log_results(self):
        """
        Report results in a file if it is setted in the config file and logs results in logs
        """
        p_uptodate = (float(self.server.nb_packages_uptodate)/float(self.server.nb_packages))*100
        p_obsolete = (float(self.server.nb_packages_obsolete)/float(self.server.nb_packages))*100
        p_unchecked = (float(self.server.nb_packages_unchecked)/float(self.server.nb_packages))*100
        
        # Put results in the log file
        self._logger.info("CentOS packages analyze results")
        self._logger.info("Number packages on server : "+str(self.server.nb_packages))
        self._logger.info("Packages up to date : [{0:.2f}%]".format(p_uptodate))
        self._logger.info("Packages obsolete : [{0:.2f}%]".format(p_obsolete))
        self._logger.info("Packages not found on the internet : [{0:.2f}%]".format(p_unchecked))
        
    def print_results(self, print_up_to_date = False):
        """
        Print analysis results
        """
        p_uptodate = (float(self.server.nb_packages_uptodate)/float(self.server.nb_packages))*100
        p_obsolete = (float(self.server.nb_packages_obsolete)/float(self.server.nb_packages))*100
        p_unchecked = (float(self.server.nb_packages_unchecked)/float(self.server.nb_packages))*100
        
        print "\n=============================================================================="
        print "==                       Packages analysis results                          =="
        print "=============================================================================="
        print "Packages number on the server : "+str(self.server.nb_packages)
        print "Packages up to date : [{0:.2f}%]".format(p_uptodate)
        print "Packages obsolete : [{0:.2f}%]".format(p_obsolete)
        print "Packages not found on the internet : [{0:.2f}%]".format(p_unchecked)
        
        print "\n=============================================================================="
        print "==                         Packages not found                               =="
        print "=============================================================================="
        print self.server.packages_unchecked
        
        print "\n=============================================================================="
        print "==                         Packages obsolete                                =="
        print "=============================================================================="
        print self.server.packages_obsolete
        
        if print_up_to_date:
            print "\n=============================================================================="
            print "==                         Packages up to dated                             =="
            print "=============================================================================="
            print self.server.packages_uptodate
        
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

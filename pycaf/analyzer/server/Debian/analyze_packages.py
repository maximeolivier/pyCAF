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
Analyze packages to check updates availables
"""
import threading
import time
import gzip
import os
import sys
import re

# Need to set the path at root project directory if necessary (doctest requirement)
if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):    
    PROJECT_PATH = os.path.dirname(os.path.abspath('../..'))
    sys.path.append(PROJECT_PATH)

import pycaf.tools as tools
import pycaf.architecture.devices.server_features as sf
import pycaf.architecture.devices as dvc

import ressources.analyzer.server as ressources

        
class AnalyzeDebianPackages (threading.Thread):
    """Download on the internet packages corresponding to the distribution and 
    check the versions
    
    >>> config = tools.ConfigParse()
    >>> lock = threading.Lock()
    >>> srv = dvc.Server()
    >>> srv.osname = "wheezy"
    >>> srv.packages = sf.PackageList()
    >>> srv.packages.add_package(sf.Package("acpitail", "0.1-4"))
    >>> srv.packages.add_package(sf.Package("invented", "42"))
    >>> srv.packages.add_package(sf.Package("acct", "6.4"))
    >>> thd = AnalyzeDebianPackages(srv, config, lock)
    >>> thd.analyze()
    True
    >>> thd.check_results()
    True
    >>> thd.log_results()
    
    """
        
    def __init__(self, server, config, lock): 
        threading.Thread.__init__(self)

        self.server = server
        self.config = config        
        self.packages = server.packages
        self.active = False
        self._logger = tools.create_logger(__name__, self.config)
        self._lock = lock
        self.config_server = ressources.ConfigServer(1)
    
    def run(self):
        self._logger.info("Run Analyze Debian Packages")
        if self.check_ressources():
            self.analyze()
            if self.check_results():
                self.log_results()
            else:
                self._logger.error("AnalyzeDebianPackages Error")
        else:
            self._logger.error("AnalyzeDebianPackages Error")
                    
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
        self._logger.info("Debian version name : " +str(self.server.osname))
        
        
        #Check if realase packages are ever stored
        #Check if the realease packages are the last version
        #Download the last realease packages of the well distribution (Lenny, wheezy,...)
            
        # Check if other packages lists availables (updates, backports,...)
        analyze_distrib_list = []
        # Get stable debian version list
#        debian_list = self.config.server_debian_stables
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
        
        
        # Inform user of packages that will be downloaded and checked        
        self._logger.info("Debian distribution packages that will be check")
        for d_1 in analyze_distrib_list:
            self._logger.info(d_1)
        
        # List of package object to analyze
        packages_list_to_analyze = self.packages.dict.values()
        packages_tmp_uptodate = []
        packages_tmp_obsolete = []
        packages_tmp_unchecked = []
        
        # Check packages algorithm
        # Step 1 : check packages with backports release packages
        # Ok -> uptodate    KO -> undetermine (uptodate or obsolete or unchecked)
        # Step 2 : check packages with updates release packages
        # Ok -> uptodate    KO -> undetermine (uptodate or obsolete or unchecked)
        # Step 3 : check name with updates release packages
        # Ok -> obsolete (backports or uptodate)    KO -> undetermine (uptodate or obsolete or unchecked)
        # Step 4 : check packages with base release packages
        # Ok -> uptodate    KO -> undetermine (obsolete or unchecked)
        # Step 5 : check name with base release packages
        # Ok -> obsolete(base)    KO -> unchecked 
        self._logger.info("Debian"+str(self.server.osname) + " packages analysis in progress...")
        
        # Regular expression to extract release package name and version
        
        # pkg_release_expression = r"(?P<pkg_name>^[A-Za-z0-9:\-~.+]+)(?P<var2> \()(?P<pkg_version>[A-Za-z0-9:\-~.+]+)(?P<var4>[ \)]{1})"
        pkg_release_expression = r"(?P<pkg_name>^[A-Za-z0-9:\-~.+]+)(?P<var2> \()(?P<pkg_version>[A-Za-z0-9:\-~,.+\[\] ]+)(?P<var4>[\)]{1})"
        pkg_release_reg = re.compile(pkg_release_expression)

        # --------------------------------------------
        # ------------------ Step 1 ------------------
        # --------------------------------------------

        distribution = analyze_distrib_list[0] 
        
        # Download packages list if necessary 
#        url = "https://packages.debian.org/fr/"+str(distribution)+\
#        "/allpackages?format=txt.gz"
        
        url = self.config_server.debian["packages_url"].replace("DISTRIBUTION", str(distribution))
        file_name = distribution + "_packages.gz"
        
        self._lock.acquire()
        download_boolean = tools.downloadFile(url, file_name, self.config, path)
        self._lock.release()
        if not download_boolean:
            self._logger.error("Download file error")
            return False
        
        # Read the file containing packages list 
        file_path = path + file_name
        f_1 = gzip.open(file_path,'rb')
        rawtext = f_1.read()
        f_1.close()
        
        # Split text in lines
        releases = rawtext.split('\n')   
        # Dictionnary of release packages
        release_dict = {}

        for l_1 in releases:
            if pkg_release_reg.match(l_1) is not None:
                result_re = pkg_release_reg.match(l_1)
                pkg_name = result_re.group('pkg_name')
                pkg_version = result_re.group('pkg_version')
                release_dict[pkg_name] = pkg_version
                     
        # We check each package with release packages
        # A PackageList object contains a dictionnary and we acceed at the package
        # object with dict.values()
        for pkg in packages_list_to_analyze:
            # Delete the ":amd64" suffix for comparaison
            if pkg.name[-6:] == ":amd64":
                pkg.name = pkg.name[:-6]

            if pkg.name in release_dict.keys():
                if pkg.version == release_dict[pkg.name]:
                    packages_tmp_uptodate.append(sf.Package(pkg.name, pkg.version, None, distribution))
                else:
                    packages_tmp_unchecked.append(pkg)
            else:
                packages_tmp_unchecked.append(pkg)
        
        # -------------------------------------------------------
        # ------------ Step 2 (and 4 with the loop) -------------
        # -------------------------------------------------------     
        
        
        for distribution in analyze_distrib_list[1:]:
            
            packages_list_to_analyze = packages_tmp_unchecked
#            packages_tmp_obsolete = []
            packages_tmp_unchecked = []
                
            # Download packages list if necessary 
#            url = "https://packages.debian.org/fr/"+str(distribution)+\
#            "/allpackages?format=txt.gz"
            url = self.config_server.debian["packages_url"].replace("DISTRIBUTION", str(distribution))
            file_name = distribution + "_packages.gz"
            
            self._lock.acquire()
            download_boolean = tools.downloadFile(url, file_name, self.config, path)
            self._lock.release()
            if not download_boolean:
                self._logger.error("Download file error")
                return False
            
      
            # Read the file containing packages list 
            file_path = path + file_name
            f_1 = gzip.open(file_path,'rb')
            rawtext = f_1.read()
            f_1.close()
            
            # Split text in lines
            releases = rawtext.split('\n')
            
            # Dictionnary of release packages
            release_dict = {}

            for l_1 in releases:
                if pkg_release_reg.match(l_1) is not None:
                    arch = self.server.kernel_release.split("-")[-1:][0]
                    result_re = pkg_release_reg.match(l_1)
                    pkg_name = result_re.group('pkg_name')
                    pkg_version = result_re.group('pkg_version')
                    elts = pkg_version.split("], ")
                    for elt in elts:
                        if ("[" + arch + "," in elt) or (" " + arch + "," in elt) or (" " + arch + "]" in elt):
                            pkg_version = elt.split(" ")[0]
                        if "[" not in elt:
                            pkg_version = elt

                    release_dict[pkg_name] = pkg_version
                         
            # We check each package with release packages
            # A PackageList object contains a dictionnary and we acceed at the package
            # object with dict.values()
            for pkg in packages_list_to_analyze:
                # Delete the ":amd64" suffix for comparaison
                if pkg.name[-6:] == ":amd64":
                    pkg.name = pkg.name[:-6]

                if pkg.name in release_dict.keys():
                    if pkg.version == release_dict[pkg.name]:
                        packages_tmp_uptodate.append(sf.Package(pkg.name, pkg.version, None, distribution))
                    else:
                        packages_tmp_obsolete.append(sf.Package(pkg.name, pkg.version, release_dict[pkg.name], distribution))

                else:
                    packages_tmp_unchecked.append(pkg)
        self._logger.debug("Nb Packages : "+str(self.packages.get_number()))
        self._logger.debug("Nb up to date : "+str(len(packages_tmp_uptodate)))
        self._logger.debug("Nb Packages obsolete : "+str(len(packages_tmp_obsolete)))
        self._logger.debug("Nb Packages unchecked : "+str(len(packages_tmp_unchecked)))
        #------------------------------------------------------------------------
        self._logger.info("Debian "+str(distribution)+" packages successfully analyzed")
 

        # Stored results and sort the list in name alphabetic order 
        self.server.packages_uptodate.push_package_list(packages_tmp_uptodate)
        self.server.packages_obsolete.push_package_list(packages_tmp_obsolete)
        self.server.packages_unchecked.push_package_list(packages_tmp_unchecked)
    
        # Fill the reporting
        self.server.nb_packages = self.packages.get_number()
        self.server.nb_packages_uptodate = self.server.packages_uptodate.get_number()
        self.server.nb_packages_obsolete = self.server.packages_obsolete.get_number()
        self.server.nb_packages_unchecked = self.server.packages_unchecked.get_number()
        
        self._logger.debug("Nb Packages : "+str(self.server.nb_packages))
        self._logger.debug("Nb up to date : "+str(self.server.nb_packages_uptodate))
        self._logger.debug("Nb Packages obsolete : "+str(self.server.nb_packages_obsolete))
        self._logger.debug("Nb Packages unchecked : "+str(self.server.nb_packages_unchecked) )
    
        
        
        end_time = time.time()
        self._logger.info("Elapsed time: "+str((end_time - start_time) * 1000)+" msecs")
        self._logger.info("Debian packages successfully analyzed !")

        
            
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
            self._logger.debug("Ressources checked for Debian package analysis")
            return True
        
    
    def check_results(self):
        """
        Check results after analyze in order to detect analysis error
        For example : number of packets is to be coherent
        """
        if self.server.nb_packages == 0:
            self._logger.error("Ckeck results : number packages = 0")
            return False
        elif ((self.server.nb_packages_obsolete + self.server.nb_packages_unchecked +self.server.nb_packages_uptodate) != self.server.nb_packages):
            self._logger.warning("Results non coherent")
            self._logger.warning("Nb Packages : "+str(self.server.nb_packages))
            self._logger.warning("Nb up to date : "+str(self.server.nb_packages_uptodate))
            self._logger.warning("Nb Packages obsolete : "+str(self.server.nb_packages_obsolete))
            self._logger.warning("Nb Packages unchecked : "+str(self.server.nb_packages_unchecked) )           
            
            return False
        else:
            self._logger.info("Packages results checked")
            return True
        
        
    
    def log_results(self):
        """
        Report formatting in order to show results at user
        """
        self._logger.info("Debian packages analyze results")
        self._logger.info("Number packages on server : "+str(self.server.nb_packages))
        
        p_uptodate = (float(self.server.nb_packages_uptodate)/float(self.server.nb_packages))*100
        self._logger.info("Packages up to date : [{0:.2f}%]".format(p_uptodate))

        p_obsolete = (float(self.server.nb_packages_obsolete)/float(self.server.nb_packages))*100
        self._logger.info("Packages obsolete : [{0:.2f}%]".format(p_obsolete))

        p_unchecked = (float(self.server.nb_packages_unchecked)/float(self.server.nb_packages))*100
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

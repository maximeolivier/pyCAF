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
Created on Mon Jun 23 14:23:48 2014

@author: thierry
"""
import threading
import time
import os
import sys
import re
import pycurl
import urllib2
import urllib
import httplib


# Need to set the path at root project directory if necessary (doctest requirement)
if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):    
    PROJECT_PATH = os.path.dirname(os.path.abspath('../..'))
    sys.path.append(PROJECT_PATH)

import pycaf.tools as tools
import pycaf.architecture.devices.server_features as sf
#import pycaf.architecture.devices as dvc
import ressources.analyzer.server as ressources

rh_sso = None
        
class AnalyzeRedHatPackages(threading.Thread):
    """Download on the internet packages corresponding to the distribution and 
    check the versions    
    """
        
    def __init__(self, server, config, lock): 
        threading.Thread.__init__(self)

        self.server = server
        self.config = config        
        self.packages = server.packages
        self.active = False
        self._logger = tools.create_logger(__name__, self.config)
        self._lock = lock
        self.config_server = ressources.ConfigServer(3)
    
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
        # Step 1 : check packages with RHEL packages
        # Ok -> uptodate    KO -> undetermine (uptodate or obsolete or unchecked)
        # Step 2 : check name with RHEL packages
        # Ok -> obsolete    KO -> unchecked
        
        # List of package object to analyze
        packages_list_to_analyze = self.packages.dict.values()
        
        # Temporary lists to manage packages
        packages_tmp_uptodate = []
        packages_tmp_obsolete = []
        packages_tmp_unchecked = []
        
        pkg_obsolete_expression = "(?P<pkg_name_start>[A-Za-z0-9:+~\-\._]+)(?P<pkg_version>(\-))"
        pkg_obsolete_reg = re.compile(pkg_obsolete_expression)
        
        # Download packages list 
        updates_list = []
        updates_list = self.request_rhel_packages()
        self._logger.info("Nb RHEL packages omported : " + str(len(updates_list)))
        
        # --------------------------------------------
        # ------------------ Step 1 ------------------
        # --------------------------------------------
    
        # tmp_list wich will be the future packages_list_to_analyze after the loop
        tmp_list = []
        for pkg in packages_list_to_analyze:
            # Add the suffix .rpm
            # ex : package.x86_64.rpm
            pkg_with_arch = pkg.name + ".rpm"

            if pkg_with_arch in updates_list or pkg_with_arch.replace(self.server.osarchitecture + ".rpm", "noarch.rpm") in updates_list:
                packages_tmp_uptodate.append(sf.Package(pkg.name, pkg.version))

            else:
                tmp_list.append(pkg)
        packages_list_to_analyze = tmp_list
        
        # --------------------------------------------
        # ------------------ Step 2 ------------------
        # --------------------------------------------
        
        # Dictionnary wich contain the start of the package and the full line
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

        packages_tmp_unchecked = tmp_list
        

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
            self._logger.error("Ckeck results : number packages = 0")
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
            
    def get_rh_sso(self):
        """
        Function wich used login and password to connect at www.redhat.com and return
        the "rh_sso" proxy used for request authentication.
        """
        self._logger.debug("RHEL rh_sso getting in progress...")
        username = self.config_server.redhat["login_username"]
        password = self.config_server.redhat["login_pass"]
        url = 'https://www.redhat.com/wapps/sso/login.html'
        values={'username':username,'password':password,'_flowId':'legacy-login-flow','redirect':'https://www.redhat.com/wapps/ugc/protected/account.html','failureRedirect':'http://www.redhat.com/wapps/sso/login.html'}
        data_post = urllib.urlencode(values)
      
        headers = Storage()
        
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
#==============================================================================
#     DEBUG comments in order to use the Burp Proxy software 
#==============================================================================
    #c.setopt(pycurl.PROXY, '127.0.0.1')
    #c.setopt(pycurl.PROXYPORT, 8080)
    #c.setopt(pycurl.SSL_VERIFYPEER, 1)
    #c.setopt(pycurl.SSL_VERIFYHOST, 2)
    #c.setopt(pycurl.CAINFO, "/home/thierry/Divers/Burp/cacert.crt")
#==============================================================================
        c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0")
        c.setopt(pycurl.HTTPHEADER, ['Accept-Language: en-US,en;q=0.5',
                                     'Connection: keep-alive',
                                     'www.whitehouse.gov: 200'])
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data_post)
        
        c.setopt(c.HEADERFUNCTION, headers.store)
        
        c.perform()
        c.close()
        headers = str(headers)
        
        expression = r"(?P<var1>.*)(?P<rh_sso>Set-Cookie: rh_sso=)(?P<sso_key>(?!\").*?)(?P<end>;)"
        header_lines = headers.split('\n')
        for head in header_lines:
            result_re = re.match(expression, head)
            
            if result_re is not None:
                sso_key = "rh_sso=" + str(result_re.group('sso_key'))
        self._logger.debug("rh_sso value : "+ str(sso_key))
        return sso_key
        
    def request_rhel_packages(self):
        import json
        global rh_sso
        answer = None
        rhel_packages_list = []
        
        if rh_sso is None: 
            rh_sso = self.get_rh_sso()
            print "Get rh_sso : " + str(rh_sso)
        
        self._logger.debug("RHEL database for packages requesting...")
        # nb_to_display at '-1' to get all packages
        nb_to_display = '-1'
        version = str(self.server.osversion[0])
        architecture = str(self.server.osarchitecture)
        req = urllib2.Request('https://access.redhat.com/downloads/content/69/ver=/rhel---' + version + '/' + architecture + '/binary/packages-datatable?sEcho=3&iColumns=6&sColumns=&iDisplayStart=0&iDisplayLength=' + nb_to_display + '&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=false&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=false&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=false')
        req.add_header('Host', 'access.redhat.com')
        req.add_header("Cookie", rh_sso)
        
        try: 
            answer = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            self._logger.error('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            self._logger.error('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            self._logger.error('HTTPException')
        except Exception:
            import traceback
            self._logger.error('generic exception: ' + traceback.format_exc())
        if answer is not None:
            answer = str(answer.read())
        else:
            return False
            
        data = json.loads(answer)
    
        expression = r"(?P<var1>.*/)(?P<package>.*.rpm)"
    
        for i in range(len(data['aaData'])):
            # 4 = comments
            result_re = re.match(expression, data['aaData'][i][5])
            if result_re is not None:
                rhel_packages_list.append(result_re.group('package'))
        rhel_packages_list.sort()     
        return rhel_packages_list
        
        
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    

class Storage:
    def __init__(self):
        self.contents = ''
     
    def store(self, buf):
        self.contents += "%s"%(buf)
     
    def __str__(self):
        return self.contents

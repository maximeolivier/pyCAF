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
Created on Tue Jul  8 09:23:27 2014

@author: thierry
"""
import pycaf.architecture.devices.server_features.windows as sw
import urllib2
import re

import threading
import time
import pycaf.tools as tools
import pycaf.architecture.devices.server_features as sf

import ressources.analyzer.server as ressources
        
class AnalyzeWindowsKB (threading.Thread):
    """
    Download on the internet KB corresponding to the distribution and 
    check with KB installed on the audited server.    
    """
        
    def __init__(self, server, config, lock): 
        threading.Thread.__init__(self)

        self.server = server
        self.config = config        
        self.kb_patches = server.kb_patches
        self._logger = tools.create_logger(__name__, self.config)
        self._lock = lock
        self.config_server = ressources.ConfigServer(4)
    
    def run(self):
        self._logger.info("Run Analyze Windows KB")
        if self.check_ressources():
            self.analyze()
            if self.check_results():
                if self.config.server_results_save_in_file or self.config.save_reports_in_file:
                    self.log_results()
                return True
            else:
                self._logger.error("Analyze Windows KB Error")
                return False
        else:
            self._logger.error("Analyze Windows KB Error")
            return False
                    
    def analyze(self):
        """
        Core function which is called in the run
        Do the effective work
        """
        start_time = time.time()
        
        # Check KB algorithm
        # Step 1 : Get OS number corresponding to the osname on the internet
        # Step 2 : download KB on the internet through the OS number
        # Step 3 : check KB on the server with the internet list
        # Ok -> uptodate    KO -> obsolete
        # Step 4 : Put KB not installed with the status : to_install
        
    
        # --------------------------------------------
        # ------------------ Step 1 ------------------
        # --------------------------------------------
        os_number = self.get_os_number(self.server.osname, self._logger)
        if not os_number:
            self._logger.error("Failed to get OS number, KB analysis failed")
            exit(1)
        
        # --------------------------------------------
        # ------------------ Step 2 ------------------
        # --------------------------------------------
        kb_uptodate_microsoft = self.get_KB_microsoft(os_number, self._logger)
        if len(kb_uptodate_microsoft) < 1:
            self._logger.error("Import KB from microsoft failed")
            exit(1)
        
        # --------------------------------------------
        # ------------------ Step 3 ------------------
        # --------------------------------------------
        
        kb_tmp_not_installed = kb_uptodate_microsoft
        kb_tmp_uptodate = []
        
        for kb_installed in self.kb_patches.dict.values():
            not_found = True
            i = 0
            while (not_found and i < len(kb_uptodate_microsoft)):
                if str(kb_installed.id) == kb_uptodate_microsoft[i].id:
                    not_found = False
                    kb_tmp_uptodate.append(kb_uptodate_microsoft[i])
                    del kb_tmp_not_installed[i]
                i += 1
            if not_found is True:
                self.server.kb_obsolete.add_kb(kb_installed)
            
        for kb_to_inst in kb_tmp_not_installed:
            self.server.kb_not_installed.add_kb(kb_to_inst)

        self.server.kb_uptodate.push_kb_list(kb_tmp_uptodate)       
#        tpT = sorted(tpT, key=lambda kb_uptodate: datetime.datetime.strptime(kb_uptodate.date, '%d/%m/%Y'), reverse = True)
        

    
        # Fill the reporting
        self.server.nb_kb = self.server.kb_patches.counter
        self.server.nb_kb_uptodate = self.server.kb_uptodate.counter
        self.server.nb_kb_obsolete = self.server.kb_obsolete.counter
        self.server.nb_kb_not_installed = self.server.kb_not_installed.counter
        
        self._logger.debug("Nb KB : "+str(self.server.nb_kb))
        self._logger.debug("Nb KB up to date : "+str(self.server.nb_kb_uptodate))
        self._logger.debug("Nb KB obsolete : "+str(self.server.nb_kb_obsolete))
        self._logger.debug("Nb KB to sinstall : "+str(self.server.nb_kb_not_installed))
    
        end_time = time.time()
        self._logger.info("Elapsed time: "+str((end_time - start_time) * 1000)+" msecs")
        self._logger.info("Windows server KB successfully analyzed !")       
            
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
        elif self.kb_patches.counter == 0:
            self._logger.error("Empty KB list : check your imported KB list")
            return False
        else:
            self._logger.debug("Ressources checked for Windows server KB analysis")
            return True
        
    
    def check_results(self):
        """
        Check results after analyze in order to detect analysis error
        For example : number of packets is to be coherent
        """
        if self.server.nb_kb == 0:
            self._logger.error("Check results : number KB = 0")
            return False
        elif ((self.server.nb_kb_uptodate + self.server.nb_kb_obsolete) != self.server.nb_kb):
            self._logger.warning("Results non coherent")
            self._logger.warning("Nb KB : "+str(self.server.nb_kb))
            self._logger.warning("Nb up to date : "+str(self.server.nb_kb_uptodate))
            self._logger.warning("Nb KB obsolete : "+str(self.server.nb_kb_obsolete))          
            return False
        else:
            self._logger.info("KB results checked")
            return True
        
        
    
    def log_results(self):
        """
        Report results in a file if it is setted in the config file and logs results in logs
        """     
        
        p_uptodate = (float(self.server.nb_kb_uptodate)/float(self.server.nb_kb))*100
        p_obsolete = (float(self.server.nb_kb_obsolete)/float(self.server.nb_kb))*100     
        
        # Put results in the log file
        self._logger.info("Windows Server analyze results")
        self._logger.info("Number KB on server : "+str(self.server.nb_kb))
        self._logger.info("KB up to date : [{0:.2f}%]".format(p_uptodate))
        self._logger.info("KB obsolete : [{0:.2f}%]".format(p_obsolete))
        
    def print_results(self, print_up_to_date = False):
        """
        Print analysis results
        """
        p_uptodate = (float(self.server.nb_kb_uptodate)/float(self.server.nb_kb))*100
        p_obsolete = (float(self.server.nb_kb_obsolete)/float(self.server.nb_kb))*100  
        
        print "\n=============================================================================="
        print "==                       KB analysis results                                =="
        print "=============================================================================="
        print "KB number on the server : "+str(self.server.nb_kb)
        print "KB up to date : [{0:.2f}%]".format(p_uptodate)
        print "KB obsolete : [{0:.2f}%]".format(p_obsolete)
        
        print "\n=============================================================================="
        print "==                         KB obsolete                                      =="
        print "=============================================================================="
        print self.server.kb_obsolete
        
        print "\n=============================================================================="
        print "==                         KB not installed                                 =="
        print "=============================================================================="
        print self.server.kb_not_installed
        
        print "\n=============================================================================="
        print "==                         KB up to dated                                   =="
        print "=============================================================================="
        print self.server.kb_uptodate

    def get_os_number(self, osname_search, logger):
        url = "https://technet.microsoft.com/fr-fr/security/bulletin"
    
        logger.info("Get on the internet the Windows Server OS number...")
        response = urllib2.urlopen(url)
        html = response.read()
        html_lines = html.split('\n')
        response.close()
        
        reg_expr = r"(?P<prev>.*?<.*?value=\")(?P<os_number>[0-9]+)(?P<separator>\">)(?P<os_name>.*?)(?P<post></option)"
        os_number = None
        
        not_found = True
        i = 0
        while (not_found and i < len(html_lines)):
            if "value" in html_lines[i] and "Windows Server" in html_lines[i]:
                result_re = re.match(reg_expr, html_lines[i])
                if result_re is not None:
                    os_name = result_re.group('os_name')
                    if os_name == osname_search:
                        os_number = str(result_re.group('os_number'))
#                        print os_number + " : " + result_re.group('os_name')
                        not_found = False
            i += 1
        if os_number is None:
            logger.error("OS number not found for : " + str(osname_search))
            return False
        else:
            logger.debug("OS number : " + str(os_number) + " for : " + str(osname_search))
            return os_number
            
    def get_KB_microsoft(self, os_number, logger):
        """
        Get list of KB for a specific Windows Server (os number) on the internet.
        """
        import httplib
        import json
        
        nb_bulletin_to_show = "10000"
        os_number = str(os_number)
        req = urllib2.Request('https://technet.microsoft.com/security/bulletin/services/GetBulletins?searchText=' + os_number + '&sortField=0&sortOrder=1&currentPage=1&bulletinsPerPage=' + nb_bulletin_to_show + '&locale=en-us')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        
        answer = None
    
        logger.info("Get on the internet the Windows Server KB database...")
        
        try: 
            answer = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            logger.error('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            logger.error('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            logger.error('HTTPException')
        except Exception:
            import traceback
            logger.error('generic exception: ' + traceback.format_exc())
            print ('generic exception: ' + traceback.format_exc())
        if answer is not None:
            answer = str(answer.read())
        else:
            return False
            
        answer = answer.decode('utf-8-sig')
        data = json.loads(answer)
        
        nb_KB = int(data['l'])
        
        kb_list = []
        for nb in range(nb_KB):
            id_kb = data['b'][nb]['KB'].encode('utf-8')
            date = data['b'][nb]['d'].encode('utf-8')
            date = date.split('/')
            date = "{:02d}/{:02d}/{:4d}".format(int(date[1]),int(date[0]),int(date[2]))
            description = data['b'][nb]['Title']
            rate = data['b'][nb]['Rating'].encode('utf-8')
            kb_list.append(sw.KBpatch(id_kb, date, description, rate))
        return kb_list
                    
        
        

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
Analyze files to check rights on it
"""
import threading
import time
import pycaf.tools as tools
import ressources.analyzer.server as ressources
        
class AnalyzeFiles (threading.Thread):
    """Check rights on all imported files    
    """
        
    def __init__(self, server, config): 
        threading.Thread.__init__(self)

        self.server = server
        self.config = config        
        self._logger = tools.create_logger(__name__, self.config)
        self.config_server = ressources.ConfigServer(0)
    
    def run(self):
        self._logger.info("Run Analyze Debian Files")
        if self.check_ressources():
            self.analyze()
            if self.check_results():
                self.log_results()
            else:
                self._logger.error("AnalyzeDebianFiles Error")
        else:
            self._logger.error("AnalyzeDebianFiles Error")
                    
    def analyze(self):
        """
        Core function which is called in the run
        Do the effective work
        """
        start_time = time.time()
        
        # Potential threat files are 777 and 660
        threat_files = self.config_server.linux["files_threat"]
        if len(self.config_server.linux["files_threat_to_hide"]) > 0:
            threat_to_hide = self.config_server.linux["files_threat_to_hide"]
            self.server.files_potentially_threat = self.server.files.filter_files(rights = threat_files, hide_path = threat_to_hide)
        else:
            self.server.files_potentially_threat = self.server.files.filter_files(rights = threat_files)
        end_time = time.time()
        self._logger.info("Debian files successfully analyzed.")
        self._logger.info("Elapsed time: {0:.2} secs".format(end_time - start_time))

        return True
    
    def check_ressources(self):
        """
        Check ressources before processing the analyze
        """
        # Check that packages list is not empty    
        if self.server.files.counter == 0:
            self._logger.error("Empty files list : check your files list")
            return False
        else:
            self._logger.debug("Ressources checked for Debian files analysis")
            return True
        
    
    def check_results(self):
        """
        Check results after analyze in order to detect analysis error
        For example : number of files is not coherent
        """
        if self.server.files_potentially_threat.counter == 0:
            test_filter = self.server.files.filter_files(rights = "-r**r**r**")
            if test_filter.counter == 0:
                self._logger.error("Files filtering function error !")
                return False
            else:
                return True
        else:
            return True
        
        
        
    
    def log_results(self):
        """
        Report formatting in order to show results at user
        """
        self._logger.info(str(self.server.files_potentially_threat.counter) + " files detected threatening")
        
    def print_results(self, print_threat_files = False):
        """
        Print analysis results
        """
        print "\n=============================================================================="
        print "==                       Files analysis results                             =="
        print "=============================================================================="
        print str(self.server.files_potentially_threat.counter) + " potentially dangerous files\n"
        
        if print_threat_files:
            self.server.files_potentially_threat.show_files()
        
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

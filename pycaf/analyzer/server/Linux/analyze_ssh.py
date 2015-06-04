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
Analyze ssh configurations to warn some inconstistence with the practice rules.
"""
import threading
import time
import pycaf.tools as tools
import pycaf.architecture.devices.server_features as sf
import ressources.analyzer.server as ressources
        
class AnalyzeSSH (threading.Thread):
    """Check the SSH configuration  
    """
        
    def __init__(self, server, config): 
        threading.Thread.__init__(self) 

        self.server = server
        self.config = config        
        self._logger = tools.create_logger(__name__, self.config)
        self.config_server = ressources.ConfigServer(0)
    
    def run(self):
        self._logger.info("Run SSH configuration checking")
        
        if self.check_ressources():
            self.analyze()
            if self.check_results():
                self.log_results()
            else:
                self._logger.error("AnalyzeDebianSSH Error")
        else:
            self._logger.error("AnalyzeDebianSSH Error")
                    
    def analyze(self):
        """
        Core function which is called in the run
        Do the effective work
        """
        start_time = time.time()
        
        # SSH model configuration
        ssh_model = sf.SSHConfig()
        ssh_model.port = self.config_server.linux["ssh"]["port"]
        ssh_model.protocol = self.config_server.linux["ssh"]["protocol"]
        ssh_model.use_privilege_separation = self.config_server.linux["ssh"]["use_privilege_separation"]
        ssh_model.log_level = self.config_server.linux["ssh"]["log_level"]
        ssh_model.permit_root_login = self.config_server.linux["ssh"]["permit_root_login"]
        ssh_model.rsa_authentication = self.config_server.linux["ssh"]["rsa_authentication"]
        ssh_model.pubkey_authentication = self.config_server.linux["ssh"]["pubkey_authentication"]
        ssh_model.permit_empty_password = self.config_server.linux["ssh"]["permit_empty_password"]
        ssh_model.password_authentication = self.config_server.linux["ssh"]["password_authentication"]
        ssh_model.x11_forwarding = self.config_server.linux["ssh"]["x11_forwarding"]
        ssh_model.use_PAM = self.config_server.linux["ssh"]["use_PAM"]
        
        self.server.ssh_config.compare_ssh_config(ssh_model)
        
        end_time = time.time()
        self._logger.info("Debian SSH configuration successfully analyzed.")
        self._logger.info("Elapsed time: {0:.2} secs".format(end_time - start_time))

        return True
    
    def check_ressources(self):
        """
        Check ressources before processing the analyze
        """
        
        if self.server.ssh_config.port is None:
            self._logger.error("Empty SSH config object : check your importation")
            return False
        else:
            self._logger.debug("Ressources checked for SSH analysis")
            return True
        
    
    def check_results(self):
        """
        Check results after analyze in order to detect analysis error
        For example : number of files is not coherent
        """
        if -1 in self.server.ssh_config.results:
            self._logger.warning("All SSH parametrers not checked !")
            return False
        else:
            return True
    
    def log_results(self):
        """
        Report formatting in order to show results at user
        """
        nb_warnings = self.server.ssh_config.results.values().count([0, 1]) + self.server.ssh_config.results.values().count([0, 0])
        self._logger.info(str(nb_warnings) + " warnings in SSH configuration")
        
    def print_results(self):
        """
        Print results of the analysis
        """
        print "=============================================================================="
        print "==                       SSH analysis results                               =="
        print "=============================================================================="
        nb_warnings = self.server.ssh_config.results.values().count([0, 1]) + self.server.ssh_config.results.values().count([0, 0])
        print str(nb_warnings) + " warnings in SSH configuration"
        print self.server.ssh_config
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

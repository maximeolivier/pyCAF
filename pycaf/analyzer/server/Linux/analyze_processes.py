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
Created on Mon May 19 14:59:46 2014

@author: thierry
"""
import threading
import pycaf.tools as tools
import pycaf.architecture.devices.server_features as sf

class AnalyzeProcesses (threading.Thread):
    """
    Filtering and analyzing processes on the host computer.
    
    """    
    def __init__(self, server, config): 
        threading.Thread.__init__(self)
        self.server = server
        self.config = config
        self._logger = tools.create_logger(__name__, self.config)
    
    def run(self):
        
        self._logger.info("Run Analyze Linux Processes")
        if self.check_ressources():
            self.analyze()
            if self.check_results():
                self.log_results()
            else:
                self._logger.error("AnalyzeDebianProcesses Error")
        else:
            self._logger.error("AnalyzeDebianProcesses Error")
            
    def check_ressources(self):
        """
        Check ressources before processing the analyze
        """
        if self.server.processes is None or self.server.processes.counter == 0:
            self._logger.error("No processes imported")
            return False
        elif self.server.connections is None or self.server.connections.counter == 0:
            self._logger.error("No connections imported")
            return False
        else:
            return True
    
    def analyze(self):
        """
        Core function which is called in the run
        Do the effective work
        """
        self.server.listening_connections = self.listening_connections()
        self.server.root_processes = self.root_process()
        self.server.listening_root_process = self.listening_root_process()
        
    def listening_connections(self):
        return self.server.connections.filter_connections(state = "LISTEN, ESTABLISHED")
        
    def root_process(self):
        return self.server.processes.filter_process(user="root", hide_ppid="0, 1, 2")

    def listening_root_process(self):
        ret = sf.ConnectionList()
        listen_ps = self.listening_connections()
        
        for connection in listen_ps.dict.values():
            ps = self.server.processes.filter_process(pid = str(connection.pid))
            if ps.counter != 1:
                self._logger.error("PID of process after filtering not unique")
                return False
            elif ps.dict[1].user == "root":
                ret.add_connection(connection)
        return ret
        
    def check_results(self):
        """
        Check results to detect if an error occured
        """
        if self.server.root_processes.counter == 0:
            self._logger.error("Root processes list is empty")
            return False
        else:
            return True
            
    def log_results(self):
        """
        Log raw analysis results
        """
        self._logger.info(str(self.server.listening_connections.counter) + " listening/connected connections")
        self._logger.info(str(self.server.root_processes.counter) + " processes executed by root")
        self._logger.info(str(self.server.listening_root_process.counter) + " listening/connected executed by root")
        
    def print_results(self):
        """
        Print analysis results
        """
        print "\n=============================================================================="
        print "==                       Processes analysis results                         =="
        print "=============================================================================="
        print str(self.server.listening_connections.counter) + " listening/connected connections"
        print str(self.server.root_processes.counter) + " processes executed by root"
        print str(self.server.listening_root_process.counter) + " listening/connected executed by root"
        
        print "\n=============================================================================="
        print "==                       Listening/connected processes                      =="
        print "=============================================================================="
        print self.server.listening_connections
        
        print "\n=============================================================================="
        print "==                       Processes executed by root                         =="
        print "=============================================================================="
        print self.server.root_processes
        
        print "\n=============================================================================="
        print "==                  Listening processes executed by root                    =="
        print "=============================================================================="
        print self.server.listening_root_process
        
        
        
        
        
        

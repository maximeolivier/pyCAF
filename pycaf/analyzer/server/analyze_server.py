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
Bandmaster for server analyzing
"""


import threading
import time
import sys
#import src
import pycaf.tools as tools
from pycaf.analyzer.server import Debian as asd
from pycaf.analyzer.server import CentOS as asc
from pycaf.analyzer.server import Linux as asl
from pycaf.analyzer.server import RedHat as asrh
from pycaf.analyzer.server import Windows as asw

        
class AnalyzeServer ():
    """Analyze a server according to predefined action rules
    
    """
        
    def __init__(self, server, config): 
        self.server = server
        self.config = config
        self.lock = threading.Lock()
        self._logger = tools.create_logger(__name__, self.config)
        
        if self.server.ostype == "Debian":
            self.analyze_debian_server()
        elif self.server.ostype == "CentOS":
            self.analyze_centos_server()
        elif self.server.ostype == "Red Hat":
            self.analyze_redhat_server()
        elif self.server.ostype == "Windows Server":
            self.analyze_windows_server()
        else:
            self._logger.error("Analyze not supported for this kinf of server : " + str(self.server.ostype))
             
    def analyze_debian_server(self):
        
        a_kernel = None
        a_packages = None
        a_process = None
        a_files = None
        a_ssh = None
        a_cron = None
        
        if "AnalyzeDebianKernel" in self.config.server_debian_scenarii:
            a_kernel = asd.AnalyzeDebianKernel(self.server, self.config, self.lock)
        if "AnalyzeDebianPackages" in self.config.server_debian_scenarii:
            a_packages = asd.AnalyzeDebianPackages(self.server, self.config, self.lock)
        if "AnalyzeProcesses" in self.config.server_debian_scenarii:
            a_process = asl.AnalyzeProcesses(self.server, self.config)
        if "AnalyzeFiles" in self.config.server_debian_scenarii:
            a_files = asl.AnalyzeFiles(self.server, self.config)
        if "AnalyzeSSH" in self.config.server_debian_scenarii:
            a_ssh = asl.AnalyzeSSH(self.server, self.config)
        if "AnalyzeCron" in self.config.server_debian_scenarii:
            a_cron = asl.AnalyzeCron(self.server, self.config)
            
        a_list = [a_kernel, a_packages, a_process, a_files, a_ssh, a_cron]
        
        start_time = time.time()
        for scenario in a_list:
            if scenario is not None:
                scenario.start()
        
        for scenario in a_list:
            if scenario is not None:
                scenario.join()
        
        stop_time = time.time()
        
        # Print reports if setted in the configuration file
        if self.config.print_reports:
            for scenario in a_list:
                if scenario is not None:
                    scenario.print_results()
        
        # Save results in a file at the logs path if setted in the configuration file
        if self.config.server_results_save_in_file or self.config.save_reports_in_file:
            file_result_name = self.server.name + "_server_report.txt"
            file_result = open(self.config.logs_path + file_result_name,"wb")
            
            orig_stdout = sys.stdout
            sys.stdout = file_result
    
            print self.server
            
            if a_ssh is not None:
                a_ssh.print_results()
            if a_packages is not None:
                a_packages.print_results(True)  
            if a_files is not None:
                a_files.print_results(True)
            if a_kernel is not None:
                a_kernel.print_results()
            if a_process is not None:
                a_process.print_results()
            if a_cron is not None:
                a_cron.print_results()
            
            sys.stdout = orig_stdout
            file_result.close()
        
        # Merge different logs files in a single file
        tools.merge_logs(self.config)
        
        print "Ellapsed time = " + str(stop_time - start_time)
        
    def analyze_redhat_server(self):
#        centos_packages = src.analyzer.CentOS.AnalyzeCentosPackages(self.server, self.config, self.lock)
        
#        a_packages = None
#        
#        a_packages = asrh.AnalyzeRedHatPackages(self.server, self.config, self.lock)
#        
#        start_time = time.time()
#        a_packages.start()
#        a_packages.join() 
#        stop_time = time.time()
#        
#        # Print reports if setted in the configuration file
#        if self.config.print_reports:
#            a_packages.print_results()
#        
#        # Save results in a file at the logs path if setted in the configuration file
#        if self.config.server_results_save_in_file or self.config.save_reports_in_file:
#            file_result_name = self.server.name + "_server_report.txt"
#            file_result = open(self.config.logs_path + file_result_name,"wb")
#            
#            orig_stdout = sys.stdout
#            sys.stdout = file_result
#    
#            print self.server
#            
#            if a_packages is not None:
#                a_packages.print_results(True)
#            
#            sys.stdout = orig_stdout
#            file_result.close()
#        
#        # Merge different logs files in a single file
#        tools.merge_logs(self.config)
#        
#        print "Ellapsed time = " + str(stop_time - start_time)
        
        a_packages = None
        a_process = None
        a_files = None
        a_ssh = None
        a_cron = None     
        
        if "AnalyzeRedHatPackages" in self.config.server_centos_scenarii:
            a_packages = asrh.AnalyzeRedHatPackages(self.server, self.config, self.lock)
        if "AnalyzeProcesses" in self.config.server_centos_scenarii:
            a_process = asl.AnalyzeProcesses(self.server, self.config)
        if "AnalyzeFiles" in self.config.server_centos_scenarii:
            a_files = asl.AnalyzeFiles(self.server, self.config)
        if "AnalyzeSSH" in self.config.server_centos_scenarii:
            a_ssh = asl.AnalyzeSSH(self.server, self.config)
        if "AnalyzeCron" in self.config.server_centos_scenarii:
            a_cron = asl.AnalyzeCron(self.server, self.config)
            
        a_list = [a_packages, a_process, a_files, a_ssh, a_cron]
        
        start_time = time.time()
        for scenario in a_list:
            if scenario is not None:
                scenario.start()
        
        for scenario in a_list:
            if scenario is not None:
                scenario.join()
        
        stop_time = time.time()
        
        # Print reports if setted in the configuration file
        if self.config.print_reports:
            for scenario in a_list:
                if scenario is not None:
                    scenario.print_results()
        
        # Save results in a file at the logs path if setted in the configuration file
        if self.config.server_results_save_in_file or self.config.save_reports_in_file:
            file_result_name = self.server.name + "_server_report.txt"
            file_result = open(self.config.logs_path + file_result_name,"wb")
            
            orig_stdout = sys.stdout
            sys.stdout = file_result
    
            print self.server
            
            if a_ssh is not None:
                a_ssh.print_results()
            if a_packages is not None:
                a_packages.print_results(True)  
            if a_files is not None:
                a_files.print_results(True)
            if a_process is not None:
                a_process.print_results()
            if a_cron is not None:
                a_cron.print_results()
            
            sys.stdout = orig_stdout
            file_result.close()
        
        # Merge different logs files in a single file
        tools.merge_logs(self.config)
        
        print "Ellapsed time = " + str(stop_time - start_time)
        
    def analyze_centos_server(self):      
        a_packages = None
        a_process = None
        a_files = None
        a_ssh = None
        a_cron = None     
        
        if "AnalyzeCentOSPackages" in self.config.server_centos_scenarii:
            a_packages = asc.AnalyzeCentosPackages(self.server, self.config, self.lock)
        if "AnalyzeProcesses" in self.config.server_centos_scenarii:
            a_process = asl.AnalyzeProcesses(self.server, self.config)
        if "AnalyzeFiles" in self.config.server_centos_scenarii:
            a_files = asl.AnalyzeFiles(self.server, self.config)
        if "AnalyzeSSH" in self.config.server_centos_scenarii:
            a_ssh = asl.AnalyzeSSH(self.server, self.config)
        if "AnalyzeCron" in self.config.server_centos_scenarii:
            a_cron = asl.AnalyzeCron(self.server, self.config)
            
        a_list = [a_packages, a_process, a_files, a_ssh, a_cron]
        
        start_time = time.time()
        for scenario in a_list:
            if scenario is not None:
                scenario.start()
        
        for scenario in a_list:
            if scenario is not None:
                scenario.join()
        
        stop_time = time.time()
        
        # Print reports if setted in the configuration file
        if self.config.print_reports:
            for scenario in a_list:
                if scenario is not None:
                    scenario.print_results()
        
        # Save results in a file at the logs path if setted in the configuration file
        if self.config.server_results_save_in_file or self.config.save_reports_in_file:
            file_result_name = self.server.name + "_server_report.txt"
            file_result = open(self.config.logs_path + file_result_name,"wb")
            
            orig_stdout = sys.stdout
            sys.stdout = file_result
    
            print self.server
            
            if a_ssh is not None:
                a_ssh.print_results()
            if a_packages is not None:
                a_packages.print_results(True)  
            if a_files is not None:
                a_files.print_results(True)
            if a_process is not None:
                a_process.print_results()
            if a_cron is not None:
                a_cron.print_results()
            
            sys.stdout = orig_stdout
            file_result.close()
        
        # Merge different logs files in a single file
        tools.merge_logs(self.config)
        
        print "Ellapsed time = " + str(stop_time - start_time)
        
    def analyze_windows_server(self):
        """
        Function wich manage all windows analyzer
        """      
        a_kb = None
        
        a_kb = asw.AnalyzeWindowsKB(self.server, self.config, self.lock)
        
        a_kb.start()
        a_kb.join() 
        
        # Print reports if setted in the configuration file
        if self.config.print_reports:
            a_kb.print_results()
            
        # Save results in a file at the logs path if setted in the configuration file
        if self.config.server_results_save_in_file or self.config.save_reports_in_file:
            file_result_name = self.server.name + "_server_report.txt"
            file_result = open(self.config.logs_path + file_result_name,"wb")
            
            orig_stdout = sys.stdout
            sys.stdout = file_result
    
            print self.server
            a_kb.print_results()
            
            sys.stdout = orig_stdout
            file_result.close()
        
        # Merge different logs files in a single file
        tools.merge_logs(self.config)

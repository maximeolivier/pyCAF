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
Created on Thu Apr 17 11:29:23 2014

@author: thierry
"""
import ConfigParser
import os
import sys
"""
Tool file which manage configuration based on the config file :
pycaf.conf
"""
# Configuration filename in the parent directory (ex : pycaf.conf) 
FILENAME = "/pycaf.conf"


class GeneralConfigParse():
    """
    This class have a constructor with arguments wich are configured by a config file
    It contains a "load_config" function wich load all configurations setted in pycaf.conf.
    relative_path : put the relative path from the root project directory
    """
    def __init__(self, relative_path = None):
        self.config = None
        
        # Section REPORTING
        self.print_reports = None
        self.save_reports_in_file = None
        
        # Section PATH
        self.ressources_path = None
        
        # Section LOGS
        self.logs_path = None
        self.logs_level = None
        self.logs_file_name = None
        
        # Section SERVER
        self.server_results_save_in_file = None
        self.file_size_warning = None
        self.server_debian_scenarii = None
        self.server_centos_scenarii = None
        self.server_rhel_scenarii = None
        
        self.load_general_config()

    def load_general_config(self):
        """
        Function which put configuration information of a file in a config object
        """
    
        self.config = ConfigParser.ConfigParser()

        # Get the path of the conf file (2 previous directory)
        pathConfFile = os.path.dirname(__file__) + "/../.."
        pathConfFile += FILENAME


        if not os.path.isfile(pathConfFile):
            print "Configuration file not fount : " + str(pathConfFile)
            sys.exit(1)
        
        try:
            self.config.read(pathConfFile)
        except ConfigParser.Error:
            print "Unable to read the configuration file"
            print "Path configuration file" + str(pathConfFile)
        
        self.print_reports = self.get_boolean_config("REPORTING", "print_reports")
        self.save_reports_in_file = self.get_boolean_config("REPORTING", "save_reports_in_file")
        
        self.ressources_path = self.get_config("PATH", "ressources_path")
        self.logs_path = self.get_config("LOGS", "logs_path")
        self.logs_level = self.get_config("LOGS", "logs_level")
        self.logs_file_name = self.get_config("LOGS", "logs_file_name")
        
        self.server_results_save_in_file = self.get_boolean_config("SERVER", "save_results_in_file")
        self.file_size_warning = float(self.get_config("SERVER", "files_size_warning_limit"))*1e6
        self.server_debian_scenarii = self.get_config_list("SERVER", "debian_scenarii")
        self.server_centos_scenarii = self.get_config_list("SERVER", "centos_scenarii")
        self.server_rhel_scenarii = self.get_config_list("SERVER", "rhel_scenarii")
        
#                else:
#            print "get cwd : " +str(os.getcwd())
#            print "abspath : " + str(os.path.dirname(__file__))
#            pathConfFile = os.path.dirname(__file__) + "/.." + relative_path

    def get_config(self, section, param):
        """
        Function which return an information corresponding the section and the parameter
        See the ConfigParser python module for more explanation.
        """
        
        ret = None
        try:
            ret = self.config.get(section, param)
        except ConfigParser.Error:
            print "Argument not found " + str(param) + " in section : " + str(section)
        
        return ret    
        
    def get_boolean_config(self, section, param):
        """
        Get a config and return True if param setted at YES or False at NO
        """
        raw_config = self.get_config(section, param)
        if raw_config.lower() == "yes":
            return True
        elif raw_config.lower() == "no":
            return False
        else:
            return None
            

        
            
    def get_config_list(self, section, param):
        """
        Function wich return a list of config separated by comas according to the section and param
        """
        params = self.config.get(section , param)
        params_list = params.split(',')
        # Remove spaces in names
        for i,name in enumerate(params_list):
            params_list[i] = name.strip()
        return params_list
        

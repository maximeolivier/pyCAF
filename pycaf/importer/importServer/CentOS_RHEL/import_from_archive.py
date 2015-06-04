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
Created on Tue Apr  8 09:36:03 2014

@author: thierry
"""
import re
import os
import pycaf.architecture.devices.server_features as sf
from pycaf.architecture.devices.server import Server

import pycaf.tools as tools
from pycaf.importer.importServer import Linux



def Import_CentOS_RHEL_server_archive(filename, config):
    """ Create a Server object from an extraction script result archive
    """
    import time

    logger = tools.create_logger(__name__, config)
    
    server_to_import = Server()

    startTime = time.time()
    
    [tmp_path, xtract_dir] = Linux.extract_archive(server_to_import, logger, filename)

    logger.info("\nServer hostname : " + str(server_to_import.name))
    
    Linux.import_version_script(server_to_import, xtract_dir, logger)

    import_osname(server_to_import, xtract_dir, logger)
    import_osversion(server_to_import, xtract_dir, logger)
    import_kernel_release(server_to_import, xtract_dir, logger)

    Linux.import_interfaces(server_to_import, xtract_dir, logger)    
    Linux.import_accounts(server_to_import, xtract_dir, logger)
    Linux.import_connections(server_to_import, xtract_dir, logger)
    Linux.import_processes(server_to_import, xtract_dir, logger)
    Linux.import_files(server_to_import, xtract_dir, logger, config)
    Linux.import_nsswith(server_to_import, xtract_dir, logger)
    Linux.import_ssh_config(server_to_import, xtract_dir, logger)
    Linux.import_sudoers(server_to_import, xtract_dir, logger)
    Linux.import_fstab(server_to_import, xtract_dir, logger)
    Linux.import_crontab(server_to_import, xtract_dir, logger, "/var/spool/cron")
    Linux.import_ip_hostname_local(server_to_import, xtract_dir, logger)
    
    import_packages(server_to_import, xtract_dir, logger)

    Linux.remove_extracted_archive(tmp_path, logger)

    endTime = time.time()
    logger.info("Server successfully imported. Time : {0:.2} secs\n".format(endTime - startTime))
    return server_to_import
       
def import_osname(server_to_import, xtract_dir, logger):
    # OS name extraction of /etc/redhat-release
    os_name_file = xtract_dir + "/etc/redhat-release"
    
    if os.path.isfile(os_name_file):
        f_os_name = open(os_name_file, 'rb')
        os_name_string = f_os_name.readline()
        f_os_name.close()

        server_to_import.osname = os_name_string
        if server_to_import.osname is None:
            logger.error("OS name detection error")
        else:
            logger.info("OS detected : " + str(server_to_import.osname))
            if "Red Hat" in server_to_import.osname:
                server_to_import.ostype = "Red Hat"
                logger.info("OS type : " + str(server_to_import.ostype))
            elif "CentOS" in server_to_import.osname:
                server_to_import.ostype = "CentOS"
                logger.info("OS type : " + str(server_to_import.ostype))
            else:
                logger.error("OS type not found in import_osname function")
    
    else:
        logger.warning("Failed importation /etc/redhat-release: unable to found a valid file") 

def import_osversion(server_to_import, xtract_dir, logger):
    # Extraction of osversion
    osversionfile = xtract_dir + "/etc/redhat-release"
    
    if os.path.isfile(osversionfile):
        f = open(osversionfile, 'rb')
        server_to_import.osversion = f.readline().rstrip()
        logger.info("OS version : " + str(server_to_import.osversion))
        f.close()
    else:
        logger.warning("Failed importation /etc/debian_version : unable to found a valid file")
        
    # OS name extraction of /etc/redhat-release
    osversionfile = xtract_dir + "/etc/redhat-release"
    
    if os.path.isfile(osversionfile):
        f_os_name = open(osversionfile, 'rb')
        os_name_string = f_os_name.readline()
        f_os_name.close()

        if os_name_string is None:
            logger.error("OS version detection error")
        else:
            version_expression = r"(?P<var1>.*?)(?P<version>[0-9]+\.[0-9]+)"
            re_result = re.match(version_expression, os_name_string)
            if re_result is None:
                logger.error("OS version detection error : unable to find a version with the regular expression")
            else:
                server_to_import.osversion = re_result.group('version')
                logger.info("OS version : " + str(server_to_import.osversion))
    
    else:
        logger.warning("Failed importation /etc/redhat-release: unable to found a valid file") 
    
def import_kernel_release(server_to_import, xtract_dir, logger):
    # Extraction of kernel_release in uname.txt
    unamefile = xtract_dir + "/uname.txt"
    
    if os.path.isfile(unamefile):
        f_2 = open(unamefile, 'rb')
        kernel_line = f_2.readline()
        f_2.close()
        server_to_import.kernel_release = kernel_line.split(' ')[2]
        server_to_import.kernel_version_running = "None"
        server_to_import.osarchitecture = kernel_line.split(' ')[-2]
        logger.info("OS architecture : " + str(server_to_import.osarchitecture))
        logger.info("Kernel release : " + str(server_to_import.kernel_release))
    else:
        logger.warning("Failed importation /uname.txt : unable to found a valid file")
    
def import_packages(server_to_import, xtract_dir, logger):
    """
    Import CentOS/RHEL packages
    """
    import subprocess
    # Import packages contained in "pkg_list.txt"
    pkg_file = xtract_dir + "/pkg_list.txt"    
    
    if os.path.isfile(pkg_file):  
        f = open(pkg_file, 'rb')
        rawtext = f.read()
        f.close()
        
        lines = rawtext.split('\n')
        
        #tmp package building
        server_to_import.packages = sf.PackageList()
        
        pkg_expression = "(?P<pkg_name>^[A-Za-z0-9:\-~.+_]+)(?P<var2>\s+)"
        pkg_reg = re.compile(pkg_expression)
    
        for l in lines:
            if pkg_reg.match(l) is not None:
                result_re = pkg_reg.match(l)
                pkg_name = result_re.group('pkg_name')
                pkg_version = None
                
                if pkg_name.startswith("kernel-"):
                    server_to_import.kernel_version_installed = pkg_name.replace("kernel-","")
                        
                server_to_import.packages.add_package(sf.Package(pkg_name, pkg_version))
                
        # Check importation with a wc linux command
        grep_wc = subprocess.check_output(('wc', '-l', str(pkg_file)))
        grep_wc = int(grep_wc.split(' ')[0])
        if grep_wc != server_to_import.packages.get_number():
            logger.error("CentOS packages importation error. Count mismatching with grep linux command")
            logger.error("Imported : " + str(server_to_import.packages.get_number()) + " Lines number in the file : " + str(grep_wc))
        else:
            logger.info(str(server_to_import.packages.get_number()) + " packages imported.")

    else:
        logger.warning("Failed importation /pkg_list.txt : unable to found a valid file")

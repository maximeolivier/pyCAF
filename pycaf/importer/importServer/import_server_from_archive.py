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
Created on Thu Jul 17 10:01:44 2014

@author: thierry
Function which find out the OS and import the archive
"""
import os
import pycaf.tools as tools
from pycaf.importer.importServer import Debian
from pycaf.importer.importServer import Windows
from pycaf.importer.importServer import CentOS_RHEL
import pycaf.architecture as archi
import pycaf.architecture.devices as devices

def Import_server_from_archive(filename, config):
    """
    Function which detect the OS from an archive and extract the server
    Return server_to_import
    """
    logger = tools.create_logger(__name__, config)
    os_number = detect_OS(filename, config)
    if os_number == 0:
        logger.error("Unable to determine the server OS : " + filename)
        return None
        
    else:
        server_to_import = None
        if os_number == 1:
            server_to_import = Windows.Import_Windows_server_archive(filename, config)
        elif os_number == 2:
            server_to_import = Debian.Import_Debian_server_archive(filename, config)
        elif os_number == 3:
            server_to_import = CentOS_RHEL.Import_CentOS_RHEL_server_archive(filename, config)
        else:
            logger.error("Unable to determine the OS but os_number not 0 :" + filename)
        return server_to_import

def Import_servers_from_folder(foldername, config):
    """ 
    Function which import several server archives in a folder
    """
    logger = tools.create_logger(__name__, config)
    
    if os.path.isdir(foldername):
        architecture_to_import = archi.Architecture()
        architecture_to_import.servers = devices.ServerList()
        file_list = os.listdir(foldername)
        for file_elem in file_list:
            path = os.path.join(foldername, file_elem)
            srv = Import_server_from_archive(path, config)
            architecture_to_import.servers.add_server(srv)
            
        create_ip_hostname_common(architecture_to_import)
        logger.info(str(architecture_to_import.servers.counter) + " servers imported from the folder : " + str(foldername))
        
        tools.merge_logs(config)
        return architecture_to_import

    else:
        logger.error("Folder not found")
        return False
    
    
def detect_OS(filename, config):
    """ 
    Function which detect an OS from the archive
    Return an integer:
    1 : Windows Server
    2 : Debian
    3 : Red Hat or CentOS
    0 : not found
    """
    import tarfile
    import zipfile
    import tempfile
    import shutil
    
    logger = tools.create_logger(__name__, config)
    
    # Step 1 : zip file -> Windows Server [1] else Linux
    # Step 2 (Linux) 
    # /etc/debian_version exist -> Debian [2]
    # Step 3
    # /etc/redhat-release exist -> CentOS or Red Hat [3]
    
    # Step 1
    if zipfile.is_zipfile(filename):
        return 1
    else:
        try:
            tarfile.is_tarfile(filename)
            tmp_path = tempfile.mkdtemp()
            # 1 - decompress archive
            compressed = tarfile.open(filename)
            compressed.extractall(tmp_path)
            # Get extraction directory name and server hostname
            for (dirname, dirnames, filenames) in os.walk(tmp_path):
                if len(dirnames) != 1:
                    raise tarfile.ExtractError("Unknown archive format")
                hostname = dirnames.pop()
                tmp_xtract_dir = os.path.join(tmp_path, hostname)
                if os.path.isdir(tmp_xtract_dir):
                    xtract_dir = tmp_xtract_dir
            # Extraction of the /etc archive if applicable
            etc = os.path.join(xtract_dir, "etc.tar.bz2")
            comp = tarfile.open(etc)
            comp.extractall(xtract_dir)
            
            # Step 2
            # Debian
            if os.path.isfile(os.path.join(xtract_dir, "etc/debian_version")):
                shutil.rmtree(tmp_path)
                return 2
            elif os.path.isfile(os.path.join(xtract_dir, "etc/redhat-release")):
                shutil.rmtree(tmp_path)
                return 3
            else:
                logger.error("Unable to determine the OS, no useful file found in etc/")
                shutil.rmtree(tmp_path)
                return 0
            
        except IOError:
            if os.path.isdir(filename):
                if os.path.isfile(os.path.join(filename, "ps2.txt")):
                    return 1
                elif os.path.isfile(os.path.join(filename, "etc/debian_version")):
                    return 2
                elif os.path.isfile(os.path.join(filename, "etc/redhat-release")):
                    return 3
                else:
                    logger.error("Folder found but impossible to found a matching file for OS detection")
            else:
                logger.error("Path is neither an archive or a folder, check your path")
                return 0
                
def create_ip_hostname_common(architecture):
    """
    Function which get each ip_hostname_local dictionnay of servers to create a single
    ip_hostname_common dictionnary. Next, it is used to update hostname attribut of 
    servers connections
    """
    for server in architecture.servers.dict.values():
        if server.interfaces.counter > 0:
            for ip, host in server.ip_hostname_local.items():
                if ip not in architecture.ip_hostname_dict:
                    architecture.ip_hostname_dict[ip] = host
    
    for server in architecture.servers.dict.values():
        server.ip_hostname_common = architecture.ip_hostname_dict
        for connection in server.connections.dict.values():
            if connection.src_ip in server.ip_hostname_local:
                connection.src_hostname = server.ip_hostname_local[connection.src_ip]
            elif connection.src_ip in server.ip_hostname_common:
                connection.src_hostname = server.ip_hostname_common[connection.src_ip]
                
            if connection.dst_ip in server.ip_hostname_local:
                connection.dst_hostname = server.ip_hostname_local[connection.dst_ip]
            elif connection.dst_ip in server.ip_hostname_common:
                connection.dst_hostname = server.ip_hostname_common[connection.dst_ip]

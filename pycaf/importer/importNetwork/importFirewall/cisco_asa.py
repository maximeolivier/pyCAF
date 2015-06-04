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
Created on Thu Aug  7 17:46:26 2014

@author: thierry
"""

import os

from pycaf.importer.importNetwork import functions as nf

from pycaf.architecture.devices.switch import Switch

import pycaf.tools as tools

def Import_cisco_switch_file(filename, config):
    """ Create a Server object from an extraction script result archive
    """
    import time

    logger = tools.create_logger(__name__, config)
    
    switch_to_import = Switch()

    startTime = time.time()
    

    if not os.path.isfile(filename):
        logger.error("Cisco switch import error, file not foud : " + str(filename))
        return False
    else:
        switch_to_import.name = filename.split('/')[-1]
        switch_to_import.manufacturer = "Cisco"
        
#        Open the file and store lines in a list
        file_switch = open(filename, 'rb')
        file_content_lines = file_switch.readlines()
        file_switch.seek(0, 0)
        file_content_exclamation = file_switch.read().split('!\n')
        file_switch.close()
        
        nf.import_cisco_hostname(switch_to_import, file_content_lines, logger)
        nf.import_cisco_osversion(switch_to_import, file_content_lines, logger)
        nf.import_cisco_vlan(switch_to_import, file_content_exclamation, logger)
        nf.import_cisco_interfaces_and_switchport(switch_to_import, file_content_exclamation, logger)
        nf.import_cisco_route(switch_to_import, file_content_lines, logger)
        nf.import_cisco_catalyst_acl_table(switch_to_import, file_content_lines, logger)
        
        print switch_to_import
        print switch_to_import.acl_table
        print switch_to_import.vlan
        print switch_to_import.interfaces
        print switch_to_import.switchport
        print switch_to_import.routes
    
#        import_osname(server_to_import, xtract_dir, logger)
    
        endTime = time.time()
        logger.info("Cisco switch successfully imported. Time : {0:.2} secs\n".format(endTime - startTime))
    return switch_to_import

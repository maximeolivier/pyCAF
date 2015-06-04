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


"""
Import all modules and packages in the importer package
"""

from pycaf.importer.importServer.Debian.import_from_archive import Import_Debian_server_archive
from pycaf.importer.importServer.CentOS_RHEL.import_from_archive import Import_CentOS_RHEL_server_archive
from pycaf.importer.importServer.Linux import import_functions
from pycaf.importer.importServer.Windows.import_from_archive import Import_Windows_server_archive
from pycaf.importer.importServer.import_server_from_archive import Import_server_from_archive
from pycaf.importer.importServer.import_server_from_archive import Import_servers_from_folder

from pycaf.importer.importNetwork.importSwitch.cisco_switch import Import_cisco_switch_file

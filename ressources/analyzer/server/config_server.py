# -*- coding: utf-8 -*-

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
Created on Thu Jun 12 10:22:05 2014

@author: thierry
"""


class ConfigServer ():
    """
    Class to store settings of server in general
    @param : os_id
    0 : Linux
    1 : Debian
    2 : CentOS
    3 : Red Hat
    4 : Windows
    """

    def __init__(self, os_id):
        """
        @param : os_id
        0 : Linux
        1 : Debian
        2 : CentOS
        3 : Red Hat
        4 : Windows
        """
        # Create several dictionnaries
        self.linux = {}
        self.debian = {}
        self.centos = {}
        self.redhat = {}
        self.windows = {}

        if os_id == 0:
            self.load_linux_config()
        elif os_id == 1:
            self.load_linux_config()
            self.load_debian_config()
        elif os_id == 2:
            self.load_linux_config()
            self.load_centos_config()
        elif os_id == 3:
            self.load_linux_config()
            self.load_redhat_config()
        elif os_id == 4:
            self.load_windows_server_config()
        else:
            print "Configuration server loading error, wrong os_id"
            exit(1)

    def load_redhat_config(self):
        self.redhat["login_username"] = 'yourrhnlogin'
        self.redhat["login_pass"] = 'yourrhnpassword'

    def load_centos_config(self):
        # Packages and kernel
        self.centos["stable_versions"] = ["5.10", "6.5"]
        self.centos["packages_url_stable_version"] = "http://mirrors.atosworldline.com/public/centos/filelist.gz"

    def load_debian_config(self):
        # Packages and kernel
        self.debian["stable_versions"] = ["jessie", "jessie-updates", "jessie-backports", "jessie-backports-sloppy", "wheezy", "wheezy-updates", "wheezy-backports"]
        self.debian["unstable_versions"] = ["testing", "sid"]
        self.debian["packages_url"] = "https://packages.debian.org/fr/DISTRIBUTION/allpackages?format=txt.gz"

    def load_linux_config(self):
        # SSH good practicies configuration
        self.linux["ssh"] = {}
        self.linux["ssh"]["port"] = "22"
        self.linux["ssh"]["protocol"] = "2"
        self.linux["ssh"]["use_privilege_separation"] = "yes"
        self.linux["ssh"]["log_level"] = "INFO"
        self.linux["ssh"]["permit_root_login"] = "no"
        self.linux["ssh"]["rsa_authentication"] = "yes"
        self.linux["ssh"]["pubkey_authentication"] = "yes"
        self.linux["ssh"]["permit_empty_password"] = "no"
        self.linux["ssh"]["password_authentication"] = "no"
        self.linux["ssh"]["x11_forwarding"] = "no"
        self.linux["ssh"]["use_PAM"] = "no"

        # Files
        self.linux["files_threat"] = "-rwxrwxrwx, -rw*rw*rw*, -***rw*rw*"
        # self.linux["files_threat_to_hide"] = ""
        self.linux["files_threat_to_hide"] = "/proc"

    def load_windows_server_config(self):
        self.windows["os_list"] = ['Microsoft Windows Server 2003',
                                   'Microsoft Windows Server 2003 for Itanium-based Systems Service Pack 1',
                                   'Microsoft Windows Server 2003 for Itanium-based Systems Service Pack 2',
                                   'Microsoft Windows Server 2003 R2',
                                   'Microsoft Windows Server 2003 Service Pack 1',
                                   'Microsoft Windows Server 2003 Service Pack 2',
                                   'Microsoft Windows Server 2003 x64 Edition',
                                   'Microsoft Windows Server 2003 x64 Edition Service Pack 2',
                                   'Microsoft Windows Server 2003, Enterprise Edition for Itanium-based Systems',
                                   'Windows Server 2003 R2 Service Pack 2',
                                   'Windows Server 2003 R2 x64 Edition Service Pack 2',
                                   'Windows Server 2008 for 32-bit Systems',
                                   'Windows Server 2008 for 32-bit Systems (Server Core installation)',
                                   'Windows Server 2008 for 32-bit Systems Service Pack 2',
                                   'Windows Server 2008 for 32-bit Systems Service Pack 2 (Server Core installation)',
                                   'Windows Server 2008 for Itanium-Based Systems',
                                   'Windows Server 2008 for Itanium-Based Systems Service Pack 2',
                                   'Windows Server 2008 for x64-based Systems',
                                   'Windows Server 2008 for x64-based Systems (Server Core installation)',
                                   'Windows Server 2008 for x64-based Systems Service Pack 2',
                                   'Windows Server 2008 for x64-based Systems Service Pack 2 (Server Core installation)',
                                   'Windows Server 2008 R2 for Itanium-Based Systems',
                                   'Windows Server 2008 R2 for Itanium-Based Systems Service Pack 1',
                                   'Windows Server 2008 R2 for x64-based Systems',
                                   'Windows Server 2008 R2 for x64-based Systems (Server Core installation)',
                                   'Windows Server 2008 R2 for x64-based Systems Service Pack 1',
                                   'Windows Server 2008 R2 for x64-based Systems Service Pack 1 (Server Core installation)',
                                   'Windows Server 2012',
                                   'Windows Server 2012 (Server Core installation)',
                                   'Windows Server 2012 R2',
                                   'Windows Server 2012 R2 (server core installation)']

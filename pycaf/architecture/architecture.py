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


import pickle

class Architecture():
    """ Definition of an architecture.
    An architecture consist in a object oncluding differents components of the target (servers, firewalls, endpoints, etc.).

    >>> arch = Architecture("resources/file.tar.gz")
    >>> print arch
    resources/file.tar.gz
    >>> print arch.servers
    [serv1, serv2, serv3]
    """

    def __init__(self, name = None, servers=None, firewalls=None, endpoints=None, routers=None):
        self.name = name

        self.servers = servers
        self.ip_hostname_dict = {}
        self.firewalls = firewalls
        self.endpoints = endpoints
        self.routers = routers

    def __str__(self):
        """ Retunr a string that describes the architecture
        """
        print "Architecture name : " + str(self.name)
        print self.servers
        #print self.firewalls
        #print self.endPoints
        #print self.routers
        
        return ""

    def set_servers(self, servers):
        self.servers = servers

    def set_firewalls(self, firewalls):
        self.firewalls = firewalls

    def set_endpoints(self, endpoints):
        self.endpoints = endpoints

    def set_routers(self, routers):
        self.routers = routers

    def saveArchitecture(self, filename):
        """ Project saving based on object serialization
        """
        output = open(filename, 'wb')
        pickle.dump(self, output)
        output.close()
        return ""

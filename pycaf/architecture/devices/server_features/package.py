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

class Package():
    """ 
    Defintion of a Package
    @param name : The name of the package
    @param version : The version of this one
    @param release : Last version of this package downloaded on the internet
    @param distribution : Distribution name containing the package (wheezy, wheezy-updates, ...)
    """

    def __init__(self, name, version, release=None, distribution = None):
        self.name = name
        self.version = version
        self.release = release
        self.distribution = distribution

    def __str__(self):
        """
        Print packages attributes
        """
        if self.release is None:
            return "%s%s" %((str(self.name)).ljust(74),(str(self.version)).ljust(40)) 
        elif self.release is not None and self.distribution is not None:
            return "%s%s%s%s" %((str(self.name)).ljust(40), (str(self.version)).ljust(20),\
            (str(self.release)).ljust(20), (str(self.distribution)).ljust(20))
        else:
            return "%s%s%s" %((str(self.name)).ljust(40),\
            (str(self.version)).ljust(40), (str(self.release)).ljust(40))


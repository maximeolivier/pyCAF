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

class PackageList():
    """
    Class wich create a list of packages
    Definition of what an PackageList is
    An package list is an object use for manage multiple package into a server
    This class uses a dictionnary and a ident number is given at each package added.
    User can get a package with printing the list and pick up the ident value.
    
    Example :
    >>print myPackageList
    packageAlpha         Id : 1
    packageBeta          Id : 2
    
    >>pBeta = myPackageList.get_package(2)
    """

    def __init__(self):
        self.dict = {}
        self.counter=0

    def add_package(self, package):
        """
        Add a package at the server dictionnary
        Dictionnary model : [counter,package]
        @param package : the package to store
        """
        self.counter += 1
        self.dict[self.counter]=package
        
    def get_package(self,ident):
        """
        Return a package corresponding to the ident value
        @param ident : the number corresponding to the package
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "Package not found"
            
    def get_number(self):
        """
        Return the number of packages in the list
        """
        return len(self.dict)
        
    def push_package_list(self,listToPush):
        """
        Push a list[] containings packages in the PackageList() object
        """
        # Sort the list in alphabetic name order
        def key_name(p): return p.name
        listToPush.sort(key=key_name)
        # Put packages in the PackageList() object
        for pkg in listToPush:
            self.add_package(pkg)
            
            

    def __str__(self):
        """
        Print the list of packages with their ident
        """
        for identityNb, package in self.dict.items():
            print "{}".format(package),
            print identityNb
        return ""

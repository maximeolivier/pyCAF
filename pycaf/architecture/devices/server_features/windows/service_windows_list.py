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
Created on Mon Jul  7 10:33:38 2014

@author: thierry
"""
import pycaf.tools as tools

class ServiceWindowsList():
    """
    Class wich create a list of services
    A services list is an object use for manage multiple services into a server
    This class uses a dictionnary and a ident number is given at each services added.
    User can get a process with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter=0

    def add_service(self, service):
        """
        Add a service at the server dictionnary
        Dictionnary model : [counter,service]
        @param service : the service to store
        """
        self.counter += 1
        self.dict[self.counter]=service
        
    def get_service(self,ident):
        """
        Return a service corresponding to the ident value
        @param ident : the number corresponding to the service
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "service not found"
        
    def filter_services(self,*args, **kwargs):
        """
        Filter all services if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return services with identification numbers : 
            filter_services(4,6,8,...)
            
        Return groups with specific values :
            filter_services(keyword="arg", keword2="arg2",....)
        keywords available :
        - name
        - status
        - service_type
        - account
        example : filter_services(status="Running", service_type="Win32")
        
        keywords availables for black list:
        - hide_name
        - hide_status
        - hide_service_type
        - hide_account
        example : filter_services(status="Running", hide_service_type="Win32")
        """

        list_filtered = ServiceWindowsList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_service(elem)

        return list_filtered
            
    def show_services(self,*args, **kwargs):
        """
        Display all services if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return services with identification numbers : 
            filter_services(4,6,8,...)
            
        Return groups with specific values :
            filter_services(keyword="arg", keword2="arg2",....)
        keywords available :
        - name
        - status
        - service_type
        - account
        example : filter_services(status="Running", service_type="Win32")
        
        keywords availables for black list:
        - hide_name
        - hide_status
        - hide_service_type
        - hide_account
        example : filter_services(status="Running", hide_service_type="Win32")
        """
        list_filtered = self.filter_services(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered
            
    def label_service_list(self):
        return "\n%s%s%s%s\n" %("Name".ljust(30), "Status".ljust(15), "Service Type".ljust(15), "Owner account".ljust(25))

    def __str__(self):
        """
        Print the list of services with their ident number.
        """
        print self.label_service_list()
        
        for identityNb, srv in self.dict.items():
            print "{}".format(srv),
            print identityNb
        return ""

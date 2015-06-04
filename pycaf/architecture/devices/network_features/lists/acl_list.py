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
Created on Fri Aug  1 15:31:37 2014

@author: thierry
"""
import pycaf.tools as tools

class ACLlist():
    """Definition of what an ACLlist is
    An acl list is an object use for manage multiple acl into a network device
    This class uses a dictionnary and a ident number is given at each acl added.
    User can get an acl with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_acl(self, acl):
        """
        Add an ACL at the network device dictionnary
        Dictionnary model : [counter,ACL]
        @param acl : the acl to store
        """
        self.counter += 1
        self.dict[self.counter] = acl
        
    def get_acl(self, ident):
        """
        Return an acl corresponding to the ident value
        @param ident : the number corresponding to the acl
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "ACL not found"
            
    def filter_acl(self,*args, **kwargs):
        """
        Filter all ACL if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_acl(4,6,8,...)
            
        Return accounts with specific values :
            filter_acl(keyword="arg", keword2="arg2",....)
        keywords available :
        - type : warning, integer value : idle(0), standard(1) and extended(2)
        - filter
        - protocol
        - comment
        - host : warning True of False
        - src_ip
        - src_port
        - src_mask
        - dst_ip
        - dst_port
        - dst_mask
        - active : warning True of False
        
        example : filter_acl(filter="deny", active=True)
        
        Black list some users
        keyword :
        - hide_type : warning, integer value : idle(0), standard(1) and extended(2)
        - hide_filter
        - hide_protocol
        - hide_comment
        - hide_host : warning True of False
        - hide_src_ip
        - hide_src_port
        - hide_src_mask
        - hide_dst_ip
        - hide_dst_port
        - hide_dst_mask
        - hide_active : warning True of False
        example 1 : filter_acl(hide_src_ip="192.168.1.42")
        """
        list_filtered = ACLlist()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_acl(elem)

        return list_filtered
            
    def show_acl(self,*args, **kwargs):
        """
        Show all ACL if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_acl(4,6,8,...)
            
        Return accounts with specific values :
            filter_acl(keyword="arg", keword2="arg2",....)
        keywords available :
        - type : warning, integer value : idle(0), standard(1) and extended(2)
        - filter
        - protocol
        - comment
        - host : warning True of False
        - src_ip
        - src_port
        - src_mask
        - dst_ip
        - dst_port
        - dst_mask
        - active : warning True of False
        
        example : filter_acl(filter="deny", active=True)
        
        Black list some users
        keyword :
        - hide_type : warning, integer value : idle(0), standard(1) and extended(2)
        - hide_filter
        - hide_protocol
        - hide_comment
        - hide_host : warning True of False
        - hide_src_ip
        - hide_src_port
        - hide_src_mask
        - hide_dst_ip
        - hide_dst_port
        - hide_dst_mask
        - hide_active : warning True of False
        example 1 : filter_acl(hide_src_ip="192.168.1.42")
        """
        list_filtered = self.filter_acl(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered

    def label_acl_list(self):
        return "\n%s%s%s%s%s%s%s%s%s%s%s\n" %("Type".ljust(10), "Filter".ljust(10), "Protocol".ljust(12), "Src IP".ljust(18),\
        "Src mask".ljust(18), "Src port".ljust(18), "Dst IP".ljust(18), "Dst mask".ljust(18),\
        "Dst port".ljust(18), "Active".ljust(6), "Comment".ljust(30))

    def __str__(self):
        """
        Print the list of accounts with their ident
        """
        print self.label_acl_list()
        for identityNb, acl in self.dict.items():
            print "{}".format(acl),
            print identityNb
        return ""
        

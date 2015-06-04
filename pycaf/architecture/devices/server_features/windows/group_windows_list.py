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
Created on Wed Jul  9 14:42:21 2014

@author: thierry
"""
import pycaf.tools as tools

class GroupWindowsList():
    
    """
    Class wich create a list of groups
    Definition of what an groupList is
    A groups list is an object use for manage multiple groups into a server
    This class uses a dictionnary and a ident number is given at each group added.
    User can get a process with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter=0

    def add_group(self, process):
        """
        Add a process at the server dictionnary
        Dictionnary model : [counter,process]
        @param process : the process to store
        """
        self.counter += 1
        self.dict[self.counter]=process
        
    def get_group(self,ident):
        """
        Return a group corresponding to the ident value
        @param ident : the number corresponding to the group
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "group not found"
            
    def filter_groups(self,*args, **kwargs):
        """
        Filter all groups if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return groups with identification numbers : 
            filter_groups(4,6,8,...)
            
        Return groups with specific values :
            filter_groups(keyword="arg", keword2="arg2",....)
        keywords available :
        - group
        - group_type
        - group_member
        - member_type
        - comment
        example : filter_groups(group_type="Global", member_type="User")
        
        keywords availables for black list:
        - hide_group
        - hide_group_type
        - hide_group_member
        - hide_member_type
        - hide_comment
        example : filter_groups(hide_group_type="Global", member_type="User")
        """

        list_filtered = GroupWindowsList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_group(elem)

        return list_filtered
            
    def show_groups(self,*args, **kwargs):
        """
        Display all groups if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return groups with identification numbers : 
            filter_groups(4,6,8,...)
            
        Return groups with specific values :
            filter_groups(keyword="arg", keword2="arg2",....)
        keywords available :
        - group
        - group_type
        - group_member
        - member_type
        - comment
        example : filter_groups(group_type="Global", member_type="User")
        
        keywords availables for black list:
        - hide_group
        - hide_group_type
        - hide_group_member
        - hide_member_type
        - hide_comment
        example : filter_groups(hide_group_type="Global", member_type="User")
        """
        list_filtered = self.filter_groups(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered

    def label_group_list(self):
        return "\n%s%s%s%s%s\n" %("Group".ljust(20), "GroupType".ljust(25), "GroupMember".ljust(40), "MemberType name".ljust(20), "Comment".ljust(20))

    def __str__(self):
        """
        Print the list of group with their ident number.
        """
        print self.label_group_list()
        
        for identityNb, grp in self.dict.items():
            print "{}".format(grp),
            print identityNb
        return ""

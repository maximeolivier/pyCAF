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
Created on Tue May 20 15:01:56 2014

@author: thierry
"""

class FileList():
    """Definition of what a FileList is
    A file list is an object use for manage multiple files into a server
    This class uses a dictionnary and a ident number is given at each files added.
    User can get an files with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_file(self, file_to_import):
        """
        Add a file at the server dictionnary
        Dictionnary model : [counter,file]
        @param file : the file to store
        """
        self.counter += 1
        self.dict[self.counter] = file_to_import
        
    def get_file(self, ident):
        """
        Return a file corresponding to the ident value
        @param ident : the number corresponding to the file
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "file not found"
            
#    def filter_files(self,*args, **kwargs):
#        """
#        Filter all files if any arguments or apply filter with this standard
#        Warning, prevent to put several keywords in one filtering. Prefer to apply a cascading filtering.
#        
#        No arguments : no filtering       
#        
#        Filter files with identification numbers : 
#        filter_files(4,6,8,42,...)
#        
#        Filter files with specific values :
#        filter_files(keyword="arg", keword2="arg2",....)
#        keywords available :
#        - path
#        - path_and_sons
#        - rights 
#        - user
#        - group
#        - time
#        example : filter_files(user ="root")
#        
#        A specific option is setted for rights. It is possible to put a "*"
#        in order to have a non specific matching.*
#        
#        Black list some args
#        keyword :
#        - hide_path
#        - hide_user
#        - hide_group
#        - hide_time
#        example 1 : filter_process(hide_path="/var/proc")
#        example 2 : filter_process(hide_user="/home/toto, /var/proc")
#        """
#        if len(kwargs) == 0 and len(args) == 0:
#            return self
#    
#        list_filtered = FileList()
#        
#        if len(args) != 0:
#            for nb_id in args:
#                list_filtered.add_file(self.dict[nb_id])
#        
#        if len(kwargs) != 0:
#            hide_list = ["hide_path", "hide_user", "hide_group", "hide_time"]
#            key_list = ["path", "path_and_sons", "rights", "user", "group", "time"]
#            key_called = []
#            hide_called = []
#            for key in kwargs:
#                if key in key_list:
#                    key_called.append(key)
#                elif key in hide_list:
#                    hide_called.append(key)
#                else:
#                    print "Error, parameter not found"
#                    return False
#                    
#            for ident, file_in_list in self.dict.items():
#                show = False
#                mismatch = 0
#                # kwargs key loop
#                for key in key_called:
#                    # Split the values of keys
#                    list_values = kwargs[key].split(',')
#                    # Remove spaces in names
#                    for i,name in enumerate(list_values):
#                        list_values[i] = name.strip()
#
#                    # White list filtering
#                    if key == "rights":
#                        for rights_values in list_values:
#                            if self.compare_rights(rights_values, file_in_list.rights):
#                                show = True
#                                
#                    elif key == "path_and_sons":
#                        for path_values in list_values:
#                            if file_in_list.path.startswith(path_values):
#                                show = True
#
#                    elif str(key) in key_list:
#                        if getattr(file_in_list, key) in list_values:
#                            show = True
#                            
#                    else:
#                        show = True
#                    
#                    if show == True:                    
#                        for key_hide  in hide_called:
#                            # Split the values of keys
#                            list_hide_values = kwargs[key_hide].split(',')
#                            # Remove spaces in names
#                            for i,name in enumerate(list_hide_values):
#                                list_hide_values[i] = name.strip()
#                                
#                            if str(key_hide) == "hide_path":
#                                for path_values in list_hide_values:
#                                    if file_in_list.path.startswith(str(path_values)):
#                                        show = False   
#                                    
#                            elif getattr(file_in_list, key_hide.split("_")[1]) in list_hide_values:
#                                show = False
#                    if show == False:
#                        mismatch += 1
#                                
#                if mismatch == 0:
#                    list_filtered.add_file(file_in_list)
#                    
#        return list_filtered
            
    def filter_files(self,*args, **kwargs):
        """
        Filter all files if any arguments or apply filter with this standard
        Warning, prevent to put several keywords in one filtering. Prefer to apply a cascading filtering.
        
        No arguments : no filtering       
        
        Filter files with identification numbers : 
        filter_files(4,6,8,42,...)
        
        Filter files with specific values :
        filter_files(keyword="arg", keword2="arg2",....)
        keywords available :
        - path
        - path_and_sons
        - rights 
        - user
        - group
        - time
        example : filter_files(user ="root")
        
        A specific option is setted for rights. It is possible to put a "*"
        in order to have a non specific matching.*
        
        Black list some args
        keyword :
        - hide_path
        - hide_user
        - hide_group
        - hide_time
        example 1 : filter_process(hide_path="/var/proc")
        example 2 : filter_process(hide_user="/home/toto, /var/proc")
        """
#        print "kwargs : " + str(kwargs)
        if len(kwargs) == 0 and len(args) == 0:
            return self
    
        list_filtered = FileList()
        
        if len(args) != 0:
            for nb_id in args:
                list_filtered.add_file(self.dict[nb_id])
        
        if len(kwargs) != 0:
            hide_dict = {"hide_path" : None, "hide_user" : None, "hide_group" : None, "hide_time" : None}
            show_dict = {"path" : None, "path_and_sons" : None, "rights" : None, "user" : None, "group" : None, "time" : None}

            for ident, file_in_list in self.dict.items():
                for key in kwargs:
                    if key in show_dict.keys():
                        show_dict[key] = False
                    elif key in hide_dict.keys():
                        hide_dict[key] = True
                    else:
                        print "Error, parameter not found"
                        return False

                for key, value in show_dict.items() + hide_dict.items():
                    if value is not None:
                        # Split the values of keys
                        list_values = kwargs[key].split(',')
                        # Remove spaces in names
                        for i,name in enumerate(list_values):
                            list_values[i] = name.strip()
    
                        # White list filtering
                        if key == "rights":
                            for rights_values in list_values:
                                if self.compare_rights(rights_values, file_in_list.rights):
                                    show_dict[key] = True
                                    
                        elif key == "path_and_sons":
                            for path_values in list_values:
                                if file_in_list.path.startswith(path_values):
                                    show_dict[key] = True
    
                        elif str(key) in show_dict.keys():
                            for value in list_values:
                                if getattr(file_in_list, key) == value:
                                    show_dict[key] = True
                        
                        # Black list filtering
                        elif key == "hide_path":
                            for path_values in list_values:
                                if file_in_list.path.startswith(str(path_values)):
                                    hide_dict[key] = False
                        
                        elif str(key) in hide_dict.keys():
                            if getattr(file_in_list, key.split("_")[1]) in list_values:
                                hide_dict[key] = False
                # result is a list which contain 'True' and 'False' results for different filtering parameters
                result = []
                for value in show_dict.values() + hide_dict.values():
                    if value is None:
                        result.append(True)
                    else:
                        result.append(value)
                if not False in result:
                    list_filtered.add_file(file_in_list)
                    
        return list_filtered

    def compare_rights(self, model, submit):
        """
        @param : model
        @param : submit
        Compare the rights of submit with the model. It is possible to replace a right with '*'
        example : compare_rights('-rw*rw*rw*','-rwxrw-rw-') == True
        """
        result = True
        if len(model) != 10 or len(submit) != 10:
            print "Bad rights argument"
            result = False
        
        else:
            for j, c_right in enumerate(model):
                if submit[j] != c_right and c_right != '*':
                    result = False
                    
        return result
    def show_files(self,*args, **kwargs):
        """
        Show all files if any arguments or apply filter with this standard
        
        No arguments : no filtering       
        
        Show files with identification numbers : 
        filter_files(4,6,8,42,...)
        
        Show files with specific values :
        filter_files(keyword="arg", keword2="arg2",....)
        keywords available :
        - path
        - rights 
        - user
        - group
        - time
        example : show_files(user ="root", rights="-r*xr*xr*x")
        
        A specific option is setted for rights. It is possible to put a "*"
        in order to have a non specific matching.
        """
        print self.filter_files(*args, **kwargs)
        
    def label_files_list(self):
        return "\n%s%s%s%s%s\n" % ("rights".ljust(15), "user".ljust(20), "group".ljust(20), "time modified".ljust(16), "file".ljust(60))
        
    def __str__(self):
        """
        Print the list of files with their ident
        Name : xxx Id : X
        """
        print self.label_files_list()
        for identityNb, file_to_show in self.dict.items():
            print "{}".format(file_to_show),
            print identityNb
        return ""
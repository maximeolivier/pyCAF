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
import pycaf.tools as tools

class AccountList():
    """Definition of what an AccountList is
    An accounts list is an object use for manage multiple accounts into a server
    This class uses a dictionnary and a ident number is given at each account added.
    User can get an account with printing the list and pick up the ident value.
    """

    def __init__(self):
        self.dict = {}
        self.counter = 0

    def add_account(self, account):
        """
        Add an account at the server dictionnary
        Dictionnary model : [counter,account]
        @param account : the account to store
        """
        self.counter += 1
        self.dict[self.counter] = account
        
    def get_account(self, ident):
        """
        Return an account corresponding to the ident value
        @param ident : the number corresponding to the account
        """
        if ident in self.dict.keys():
            return self.dict[ident]
        else:
            print "Account not found"
            
    def filter_accounts(self,*args, **kwargs):
        """
        Filter all accounts if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            filter_accounts(4,6,8,...)
            
        Return accounts with specific values :
            filter_accounts(keyword="arg", keword2="arg2",....)
        keywords available :
        - uid
        - name
        - group_id
        - group_name
        example : filter_accounts(uid="12")
        
        Black list some users
        keyword :
        - hide_uid
        - hide_name
        - hide_group_id
        - hide_group_name
        example 1 : filter_accounts(hide_uid="1")
        """
        list_filtered = AccountList()
        
        object_list_in = self.dict.values()
        object_list_out = tools.filter_objects(object_list_in, *args, **kwargs)
        if object_list_out is not False:
            for elem in object_list_out:
                list_filtered.add_account(elem)

        return list_filtered
            
    def show_accounts(self,*args, **kwargs):
        """
        Show all accounts if any arguments or apply filter with this standard

        No arguments : no filtering       
        
        Return accounts with identification numbers : 
            show_accounts(4,6,8,...)
            
        Show accounts with specific values :
            show_accounts(keyword="arg", keword2="arg2",....)
        keywords available :
        - uid
        - name
        - group_id
        - group_name
        example : show_accounts(uid="12")
        
        Black list some users
        keyword :
        - hide_uid
        - hide_name
        - hide_group_id
        - hide_group_name
        example 1 : show_accounts(hide_uid="1")
        """
        list_filtered = self.filter_accounts(*args, **kwargs)
        if list_filtered.counter > 0:
            print list_filtered

    def label_accounts_list(self):
        return "\n%s%s%s%s\n" %("uid".ljust(20), "username".ljust(20), "gid".ljust(20), "group name".ljust(20))
        
    def __str__(self):
        """
        Print the list of accounts with their ident
        """
        print self.label_accounts_list()
        for identityNb, account in self.dict.items():
            print "{}".format(account),
            print identityNb
        return ""
        

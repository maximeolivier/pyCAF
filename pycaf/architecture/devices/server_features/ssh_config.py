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
Created on Thu May 22 11:34:34 2014

@author: thierry

"""

class SSHConfig():
    """ 
    Definition of a SSH configuration
    
    @param port : Port used by the sshd process [default : 22]
    @param protocol : protocol number used by the service ( 1 or 2) [default : 2]
    @param use_privilege_separation : yes or no [default : yes]
    @param log_level : QUIET, FATAL, ERROR, INFO, VERBOSE, DEBUG, DEBUG1, DEBUG2, or DEBUG3 [default : INFO]
    @param permit_root_login : permit to log as root [default : yes]
    @param rsa_authentication : yes or no. Used only by protocol 1 [default : yes]
    @param pubkey_authentication : Public key used. Yes or no. Used only by protocol 2 [default : yes]
    @param permit_empty_password : yes or no. [default : no]
    @param password_authentication : use password for authentication [default : yes]
    @param x11_forwarding : graphic interface usage. Yes or no. [default : no]
    @param use_PAM : use PAM rules [default : no]
    
    @param results : list of integers wich contain the results of analysis (-1 = idle, 0 = NO OK, 1 = OK)
    """

    def __init__(self, port=None, protocol=None, use_privilege_separation=None, log_level=None,
                 permit_root_login=None, rsa_authentication=None, pubkey_authentication=None,
                 permit_empty_password=None, password_authentication=None, x11_forwarding=None,
                 use_PAM=None):
        self.port = port
        self.protocol = protocol
        self.use_privilege_separation = use_privilege_separation
        self.log_level = log_level
        self.permit_root_login = permit_root_login
        self.rsa_authentication = rsa_authentication
        self.pubkey_authentication = pubkey_authentication
        self.permit_empty_password = permit_empty_password
        self.password_authentication = password_authentication
        self.x11_forwarding = x11_forwarding
        self.use_PAM = use_PAM
        self.results = {}        
        
        arguments = ['port', 'protocol', 'use_privilege_separation', 'log_level',
                     'permit_root_login', 'rsa_authentication', 'pubkey_authentication',
                     'permit_empty_password', 'password_authentication', 'x11_forwarding', 'use_PAM']
        for arg in arguments:
            # Table to store results
            # Variable to store analysis results (-1 = idle, 0 = NO OK, 1 = OK)
            # Variable to store if default setting or imported setting (-1 = idle, 0 = default, 1 = imported)
            self.results[arg] = [-1, -1]
        
        
    def compare_ssh_config(self, ssh_config2):
        """
        Function which compare two ssh config objects and return a result list
        containings numerical values :
        0 : different
        1 : good
        """
        arguments = ['port', 'protocol', 'use_privilege_separation', 'log_level',
                     'permit_root_login', 'rsa_authentication', 'pubkey_authentication',
                     'permit_empty_password', 'password_authentication', 'x11_forwarding', 'use_PAM']
        for i, arg in enumerate(arguments):
            if getattr(self, arg) == getattr(ssh_config2, arg):
                self.results[arg][0] = 1
            else:
                self.results[arg][0] = 0
                
    def __str__(self):
        """
        Print ssh_config attributes
        """
        if [-1, -1] in self.results.values():
            return (" Port : %s\n Protocol : %s\n Use privilege separation : %s\n "
            "Log level : %s\n Permit root login : %s\n RSA authentication : %s\n "
            "Pubkey authentication : %s\n Permit empty password : %s\n "
            "Password authentication : %s\n X11 forwarding : %s\n Use PAM : %s\n"
            %(self.port, self.protocol, self.use_privilege_separation, self.log_level,
            self.permit_root_login, self.rsa_authentication, self.pubkey_authentication,
            self.permit_empty_password, self.password_authentication, self.x11_forwarding,
            self.use_PAM))
        else:
            res={}
            imp={}

            res[1] = "[OK]"
            res[0] = "[WARNING]"
            res[-1] = "[UNDEFINED]"
            imp[1] = "[IMPORTED]"
            imp[0] = "[DEFAULT]"
            imp[-1] = "[UNDEFINED]"
            
            print "{:<30} {:<15} {:<15} {:<15}".format('Port', self.port, res[self.results["port"][0]], imp[self.results["port"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('Protocol', self.protocol, res[self.results["protocol"][0]], imp[self.results["protocol"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('Use privilege separation', self.use_privilege_separation, res[self.results["use_privilege_separation"][0]], imp[self.results["use_privilege_separation"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('Log level', self.log_level, res[self.results["log_level"][0]], imp[self.results["log_level"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('Permit root login', self.permit_root_login, res[self.results["permit_root_login"][0]], imp[self.results["permit_root_login"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('RSA authentication', self.rsa_authentication, res[self.results["rsa_authentication"][0]], imp[self.results["rsa_authentication"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('Pubkey authentication', self.pubkey_authentication, res[self.results["pubkey_authentication"][0]], imp[self.results["pubkey_authentication"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('Permit empty password', self.permit_empty_password, res[self.results["permit_empty_password"][0]], imp[self.results["permit_empty_password"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('Password authentication', self.password_authentication, res[self.results["password_authentication"][0]], imp[self.results["password_authentication"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('X11 forwarding', self.x11_forwarding, res[self.results["x11_forwarding"][0]], imp[self.results["x11_forwarding"][1]])
            print "{:<30} {:<15} {:<15} {:<15}".format('Use PAM', self.use_PAM, res[self.results["use_PAM"][0]], imp[self.results["use_PAM"][1]])
            
            return ""
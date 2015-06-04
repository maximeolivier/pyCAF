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
Created on Wed Jun 18 15:29:58 2014

@author: thierry
Module which contain several functions used for a Linux importation
"""
import os
import re
import pycaf.architecture.devices.server_features as sf
import pycaf.architecture as architecture

def extract_archive(server_to_import, logger, filename):
    import tarfile
    import tempfile
    
    tmp_path = None
    
    if os.path.isdir(filename):
        xtract_dir = filename
        
        if not(os.path.isdir(filename + "/etc") and os.path.isdir(filename + "/var")):
            logger.error("/etc or /var not decompressed")
            logger.error("You referenced an uncompressed directory. Please, decompressed all the content")
            exit(1)
            
        hostname = filename.split("/")[-1]
    else:
        # Prepare extraction output directory
        tmp_path = tempfile.mkdtemp()
        
        # 1 - decompress archive
        compressed = tarfile.open(filename)
        compressed.extractall(tmp_path)
        # Get extraction directory name and server hostname
        for (dirname, dirnames, filenames) in os.walk(tmp_path):
            if len(dirnames) != 1:
                raise tarfile.ExtractError("Unknown archive format")
            hostname = dirnames.pop()
            tmp_xtract_dir = os.path.join(tmp_path, hostname)
            if os.path.isdir(tmp_xtract_dir):
                xtract_dir = tmp_xtract_dir
        # Extraction of the /etc archive if applicable
        etc = xtract_dir + "/etc.tar.bz2"
        comp = tarfile.open(etc)
        comp.extractall(xtract_dir)
        os.system("chmod -R +r " + str(xtract_dir) + "/etc")
        
        var_spool_cron = xtract_dir + "/var_spool_cron.tar.bz2"
        compr = tarfile.open(var_spool_cron)
        compr.extractall(xtract_dir)
        
    server_to_import.name = hostname
    return [tmp_path, xtract_dir]
    
def remove_extracted_archive(tmp_path, logger):
    import shutil
    if tmp_path is not None :
            shutil.rmtree(tmp_path)
            logger.debug("Extracted archive removed")

def import_version_script(server_to_import, xtract_dir, logger):
    # Importation of the script version
    scriptversionfile = xtract_dir + "/version_script.txt"
    
    if os.path.isfile(scriptversionfile):
        f = open(scriptversionfile, 'rb')
        server_to_import.version_script = f.readline().rstrip()
        logger.info("Extraction script version : " + str(server_to_import.version_script))
        f.close()
    else:
       logger.warning("Failed importation /version_script.txt : unable to found a valid file")
       
def import_interfaces(server_to_import, xtract_dir, logger):
    # Import interfaces
    interface_file = xtract_dir + "/network.txt"
    
    if os.path.isfile(interface_file):    
        server_to_import.interfaces = sf.InterfaceList()
        f_interface = open(interface_file, 'rb')
        raw_interface_file = f_interface.read()
        f_interface.close()
        
        blocks_interface = raw_interface_file.split('\n\n')
        
        #Supress the last case which is empty
        blocks_interface = blocks_interface[:-1]
        
        iface_reg_expr_name = r"(?P<name>^[a-zA-Z0-9:\-\"~.+/=]+)"
        iface_reg_expr_mac = r"(?P<var1>.*?(ether|HWaddr).*)(?P<mac>([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})"
        iface_reg_expr_address = r"(?P<var1>.*?inet(?!6).*?)(?P<address>([0-9]+.){3}([0-9]+){1})"
        iface_reg_expr_inet6 = r"(?P<var1>.*?inet6:*.*?)(?P<inet6>[0-9a-fA-F:/]+)"
        iface_reg_expr_mask = r"(?P<var1>.*?(m|M)as(k|que).*?)(?P<mask>([0-9]+.){3}([0-9]+){1})"
    
        reg_iface_name = re.compile(iface_reg_expr_name)
        reg_iface_mac = re.compile(iface_reg_expr_name + iface_reg_expr_mac)
        reg_iface_address = re.compile(iface_reg_expr_address)
        reg_iface_inet6 = re.compile(iface_reg_expr_inet6)
        reg_iface_mask = re.compile(iface_reg_expr_mask)
        
        for l_iface in blocks_interface:
            l_iface = l_iface.replace('\n', '')
            interface = sf.Interface()
            match_name = reg_iface_name.match(l_iface)
            match_mac = reg_iface_mac.match(l_iface)
            match_address = reg_iface_address.match(l_iface)
            match_inet6 = reg_iface_inet6.match(l_iface)
            match_mask = reg_iface_mask.match(l_iface)
            
            if match_name is not None:
                interface.name = match_name.group('name')
            else:
                logger.error('Interface name failed to import')
            if match_mac is not None:
                interface.mac = match_mac.group('mac')
            else:
                logger.debug('Interface MAC address failed to import')
            if match_address is not None:
                interface.ip_adress = match_address.group('address')
            else:
                logger.warning('Interface IPV4 address failed to import')
            if match_mask is not None:
                interface.mask = match_mask.group('mask')
            else:
                logger.warning('Interface mask address failed to import')
            if match_inet6 is not None:
                interface.ipv6_address = match_inet6.group('inet6')
            else:
                logger.debug('Interface IPv6 address not found')
            
            # Put results into the server_to_import object        
            server_to_import.interfaces.add_interface(interface)
        logger.info(str(server_to_import.interfaces.counter) + " interfaces imported.")
    else:
        logger.warning("Failed importation /network.txt : unable to found a valid file")
        

def import_processes(server_to_import, xtract_dir, logger):
    # Import processes with the file ps-format.txt via the command [ps -axeo pid,ppid,user,args]  
    ps_file = xtract_dir + "/ps-format.txt"
    
    if os.path.isfile(ps_file):    
        server_to_import.processes = sf.ProcessList()
        f_ps = open(ps_file, 'rb')
        raw_ps_file = f_ps.read()
        f_ps.close()
        
        lines_ps = raw_ps_file.split('\n')
        
        ps_reg_expression = (r"(?P<var1>^[ ]*)(?P<pid>([0-9]+))(?P<var2>[ ]+)"
        r"(?P<ppid>[0-9]+)(?P<var3>[ ]+)(?P<user>[a-zA-Z0-9:\-_$]+)(?P<var4>[ ]+)"
        r"(?P<command>[a-zA-Z0-9:\-\"~.+/=_\<\>\[\] ]+)")
       
        ps_reg = re.compile(ps_reg_expression)
        
        for l_ps in lines_ps:
            if (ps_reg.match(l_ps) is not None):
                result_re = ps_reg.match(l_ps)
                
                server_to_import.processes.add_process(sf.Process(result_re.group('pid'),\
                result_re.group('ppid'), result_re.group('user'), result_re.group('command')))
                
        logger.info(str(server_to_import.processes.counter) + " processes imported.")
    else:
        logger.warning("Failed importation /ps-format.txt : unable to found a valid file")
        
def import_connections(server_to_import, xtract_dir, logger):
    # Import connection
    connection_file = xtract_dir + "/netstat.txt"
    
    if os.path.isfile(connection_file):
        server_to_import.connections = sf.ConnectionList()
        f_netstat = open(connection_file, 'rb')
        raw_connection_file = f_netstat.read()
        f_netstat.close()
        
        lines_connection = raw_connection_file.split('\n')
        
        connection_ext_expression = (r"(?P<proto>^[A-Za-z0-9\-]+)(?P<var2>([ ]+[0-9]+){2} )"
        r"(?P<src_ip>((([0-9]+[.]{1}){3}[0-9]+)|([0-9a-f]*[:]{1}){2}[0-9a-f]*))(?P<var3>[:]?)"
        r"(?P<src_port>[0-9]+)(?P<var5>[ ]+)"
        r"(?P<dst_ip>((([0-9]+[.]{1}){3}[0-9]+)|([0-9a-f]*[:]{1}){2}[0-9a-f]*))"
        r"(?P<var7>[:]?)(?P<dst_port>[0-9*]+)"
        r"(?P<var9>[ ]+)(?P<state>[A-Z_]*)"
        r"(?P<var10>[ ]*)(?P<pid>[0-9\-]*)(?P<var11>[/]*)(?P<program>[a-zA-Z0-9.]*)")
        
        
        connection_reg_ext = re.compile(connection_ext_expression)
        
        for l_connection in lines_connection:
            if (connection_reg_ext.match(l_connection) is not None):
                result_re = connection_reg_ext.match(l_connection)
                
                server_to_import.connections.add_connection(sf.Connection(result_re.group('proto'),\
                result_re.group('src_ip'), result_re.group('src_port'), result_re.group('dst_ip'),\
                result_re.group('dst_port'), result_re.group('state'), result_re.group('pid'), result_re.group('program')))
        
        logger.info(str(server_to_import.connections.counter) + " connections imported.")
    else:
        logger.warning("Failed importation /netstat.txt configuration : unable to found a valid file")

def import_accounts(server_to_import, xtract_dir, logger):
    # Get account list and put it in server.accounts
    # accounts list building
    
    accountFile = xtract_dir + "/etc/passwd"
    
    if os.path.isfile(accountFile):
        
        server_to_import.accounts = architecture.devices.server_features.AccountList()
        
        #Pick up raw information
        f = open(accountFile, 'rb')
        raw_account_file = f.read()
        f.close()
        
        account_group = xtract_dir + "/etc/group"
        f = open(account_group, 'rb')
        raw_group_file = f.read()
        f.close()
        
        lines_account = raw_account_file.split('\n')
        lines_group = raw_group_file.split('\n')
        
        #Regular expression
        #?P<varX> used to split the matching expression
        # Regular expression ^(start of line)[A-Za-z0-9]*(several char):(dots needs)
        account_short_expression = r"(?P<var1>^[A-Za-z0-9\-]*?)(?P<var2>:)"
        account_medium_expression = r"(?P<var1>^[A-Za-z0-9\-]*?)(?P<var2>:(x|\*):)(?P<var3>[0-9]*)(?P<var4>:)"
        account_long_expression = r"(?P<var1>^[A-Za-z0-9\-]*?)(?P<var2>:(x|\*):)(?P<var3>[0-9]*)(?P<var4>:)(?P<var5>[0-9]*)"
        account_reg_short=re.compile(account_short_expression)
        account_reg_medium=re.compile(account_medium_expression)    
        account_reg_long=re.compile(account_long_expression)
        
        # Create a dict to store the name corresponding to the gid
        dict_group_name = {}
        
        for l_group in lines_group:
            if (account_reg_medium.match(l_group) is not None):
                result_re = account_reg_medium.match(l_group)
                gname = result_re.group('var1')
                gid = result_re.group('var3')
                
                dict_group_name[gid] = gname
    
        for l_account in lines_account:
            if (account_reg_short.match(l_account) is not None) and (account_reg_long.match(l_account) is None):
                logger.warning("Warning : shadow password unused. Unable to pick up the UID account")
                logger.warning("Line = " + str(l_account))
                uid=-1
                result_re_short = account_reg_short.match(l_account)
                name = result_re_short.group('var1')
                
            elif (account_reg_long.match(l_account) is not None):
                result_re = account_reg_long.match(l_account)
                name = result_re.group('var1')
                uid = result_re.group('var3')
                gid = result_re.group('var5')
                
                # add the group name if it exists
                if gid in dict_group_name.keys():
                    server_to_import.accounts.add_account(sf.Account(uid, name, gid, dict_group_name[gid]))   #add accounts in the list 
                else:
                    server_to_import.accounts.add_account(sf.Account(uid, name, gid))   #add accounts in the list 
                    
        logger.info(str(server_to_import.accounts.counter) + " accounts imported.")
    else:
        logger.warning("Failed importation /etc/passwd configuration : unable to found a valid file") 
        
def import_files(server_to_import, xtract_dir, logger, config):
    
    #Pick up raw information
    find_file = xtract_dir + "/find.txt"
    
    if os.path.isfile(find_file):
    
        go_import = False
        # Print a warning if the file size is up to 50 MB.
        find_size = os.stat(find_file).st_size
        if find_size > config.file_size_warning :
            decision = raw_input("The size of find.txt = " + str(find_size/1e6) + " Mo. Would you like import this file ? (y/n) : ")
            if decision.lower() == "y":
                go_import = True
            elif decision.lower() == "n":
                go_import = False
            else:
                print "Value enter not allowed. Try again."
                import_files(server_to_import, xtract_dir, logger)
            
        else:
            go_import = True
        
        if go_import:       
            server_to_import.files = sf.FileList()
            f = open(find_file, 'rb')
            raw_find_file = f.read()
            f.close()
            
            # Split and suppress the last blank line.
            lines_find = raw_find_file.split('\n')
            lines_find = lines_find[:-1]
            
            #Regular expression
            #?P<varX> used to split the matching expression
            files_expression = (r"(?P<var1>^[ ]*)(?P<var2>[0-9]+)(?P<var3>[ ]+)(?P<var4>[0-9]+)"
            r"(?P<var5>[ ]+)(?P<rights>[a-z\-T]+)(?P<var6>[ ]+)(?P<var6bis>[0-9]+)(?P<var7>[ ]+)"
            r"(?P<user>[a-zA-Z0-9:\-_$]+)(?P<var8>[ ]+)(?P<group>[a-zA-Z0-9:\-_$]+)(?P<var9>[ ]+)"
            r"(?P<var9bis>([0-9]+\,[ ]+)*)"
            r"(?P<var10>[0-9]*)(?P<var11>[ ]+)(?P<month>[A-za-zäéû.]+)(?P<var12>[ ]+)(?P<day>[0-9]+)"
            r"(?P<var13>[ ]+)(?P<yearOrHour>[0-9:]+)(?P<var14>[ ]+)(?P<filename>.+$)") 
            
            file_reg = re.compile(files_expression)
            not_match = 0
            for l_find in lines_find:
                
                if (file_reg.match(l_find) is not None):
                    result_re = file_reg.match(l_find)
                    time = str(result_re.group('month')) + " " + str(result_re.group('day')) + " " + str(result_re.group('yearOrHour'))
                    server_to_import.files.add_file(sf.File(result_re.group('filename').decode('utf8'), result_re.group('rights'), result_re.group('user'), result_re.group('group'), time))
                else:
                    logger.debug("failed import : " + str(l_find))
                    not_match += 1
                    if not_match > 50:
                       logger.error("Failed importation files in find.txt") 
                       break
                    
            logger.info(str(server_to_import.files.counter) + " files imported.")
    else:
        logger.warning("Failed importation find (/ -ls) configuration : unable to found a valid file")
        
def import_nsswith(server_to_import, xtract_dir, logger):
    """
    Import the nsswitch.conf content
    Just useful information is imported (not comments)
    """
    nss_conf_file = xtract_dir + "/etc/nsswitch.conf"
    
    # Remove blank lines (\s*$) and lines which started with a #.
    nocomment_expression = r"^(?!\s*$|#)"
    nocomment_reg = re.compile(nocomment_expression)
    
    if os.path.isfile(nss_conf_file):
        file_nss = open(nss_conf_file)    
        raw_nss = file_nss.read()
        file_nss.close()
        raw_nss = raw_nss.split('\n')
        
        for l_nss in raw_nss:
            if nocomment_reg.match(l_nss):
                server_to_import.nsswitch += l_nss + "\n"
                
        logger.info(str(len(server_to_import.nsswitch.split('\n'))-1) + " nsswitch rules imported.")
                
    else:
        logger.warning("Failed importation nsswicth.conf : unable to found a valid nsswitch configuration file at /etc/nsswitch.conf location")

def import_sudoers(server_to_import, xtract_dir, logger):
    """
    Import the /etc/sudoers content
    Just useful information is imported (not comments)
    """
    sudo_conf_file = xtract_dir + "/etc/sudoers"
    
    # Remove blank lines (\s*$) and lines which started with a #.
    nocomment_expression = r"^(?!\s*$|#)"
    nocomment_reg = re.compile(nocomment_expression)
    
    if os.path.isfile(sudo_conf_file):
        file_sudo = open(sudo_conf_file,"rb")    
        raw_sudo = file_sudo.read()
        file_sudo.close()
        raw_sudo = raw_sudo.split('\n')
        
        for l_sudo in raw_sudo:
            if nocomment_reg.match(l_sudo):
                server_to_import.sudoers_config += l_sudo + "\n"              
    else:
        logger.warning("Failed importation sudoers : unable to found a valid sudoers configuration file at /etc/sudoers location")

    sudo_repo = xtract_dir + "/etc/sudoers.d"
    
    if os.path.isdir(sudo_repo):
        for sudo_file in os.listdir(sudo_repo):
            sudo_file = os.path.join(sudo_repo, sudo_file)
            if os.path.isfile(sudo_file):
                file_sudo = open(sudo_file,"rb")    
                raw_sudo = file_sudo.read()
                file_sudo.close()
                raw_sudo = raw_sudo.split('\n')
                
                for l_sudo in raw_sudo:
                    if nocomment_reg.match(l_sudo):
                        server_to_import.sudoers_config += l_sudo + "\n"
            else:
                logger.error("Cannot open the file : " + str(sudo_file))
    else:
        logger.warning("Failed importation sudoers.d content : unable to found a valid directory at /etc/sudoers.d location")
                
    logger.info(str(len(server_to_import.sudoers_config.split('\n'))-1) + " sudoers rules imported.")

def import_fstab(server_to_import, xtract_dir, logger):
    """
    Import the /etc/fstab content
    Just useful information is imported (not comments)
    """
    fstab_file = xtract_dir + "/etc/fstab"
    
    # Remove blank lines (\s*$) and lines which started with a #.
    nocomment_expression = r"^(?!\s*$|#)"
    nocomment_reg = re.compile(nocomment_expression)
    
    if os.path.isfile(fstab_file):
        file_fstab = open(fstab_file)    
        raw_fstab = file_fstab.read()
        file_fstab.close()
        raw_fstab = raw_fstab.split('\n')
        
        for l_fstab in raw_fstab:
            if nocomment_reg.match(l_fstab):
                server_to_import.fstab_config += l_fstab + "\n"
                
        logger.info(str(len(server_to_import.fstab_config.split('\n'))-1) + " fstab rules imported.")
                
    else:
        logger.warning("Failed importation fstab : unable to found a valid fstab configuration file at /etc/fstab location")

        
def import_crontab(server_to_import, xtract_dir, logger, path_to_import):
    """
    Import the /var/spool/cron/crontabs
    Just useful information is imported (not comments)
    """
#    cron_dir = xtract_dir + "/var/spool/cron/crontabs"
    cron_dir = xtract_dir + path_to_import
    
    # Remove blank lines (\s*$) and lines which started with a #.
    nocomment_expression = r"^(?!\s*$|#|[A-Z])"
    #r"^(?!\s*$|#)"
    nocomment_reg = re.compile(nocomment_expression)
    
    ct_rules = 0
    
    if os.path.isdir(cron_dir):
        for file_user in os.listdir(cron_dir):
            server_to_import.crontab_config[file_user] = ""
            file_cron = open(cron_dir + "/" + file_user)    
            raw_cron = file_cron.read()
            file_cron.close()
            raw_cron = raw_cron.split('\n')
            
            for l_cron in raw_cron:
                if nocomment_reg.match(l_cron):
                    server_to_import.crontab_config[file_user] += l_cron + "\n"
                    ct_rules += 1
        server_to_import.crontab_rules_counter = ct_rules
        logger.info(str(ct_rules) + " cronatb rules imported.")
                
    else:
        logger.error("Failed importation crontab : unable to found a valid crontab configuration file at " + str(path_to_import))
        
def import_ssh_config(server_to_import, xtract_dir, logger):
    """
    Import the ssh configuration contained in the /etc/ssh/sshd_config file.
    Create and fullfill a ssh_config object (see the server_features package)
    """
    sshd_file = xtract_dir + "/etc/ssh/sshd_config"
    count = 0
    
    if os.path.isfile(sshd_file):
        re_port = re.compile("(?P<label>^Port\s+)(?P<port>[0-9]+)")
        re_protocol = re.compile("(?P<label>^Protocol\s+)(?P<protocol>[0-9]+)")
        re_privilege_separation = re.compile("(?P<label>^UsePrivilegeSeparation\s+)(?P<priv_sep>[a-z]+)")
        re_loglevel = re.compile("(?P<label>^LogLevel\s+)(?P<log_level>[A-Z0-9]+)")
        re_permit_root_login = re.compile("(?P<label>^PermitRootLogin\s+)(?P<root_login>[a-z]+)")
        re_rsa_auth = re.compile("(?P<label>^RSAAuthentication\s+)(?P<rsa_auth>[a-z]+)")
        re_pubkey_auth = re.compile("(?P<label>^PubkeyAuthentication\s+)(?P<pubkey_auth>[a-z]+)")
        re_permit_empty_psswd = re.compile("(?P<label>^PermitEmptyPasswords\s+)(?P<perm_empty_psswd>[a-z]+)")
        re_psswd_auth = re.compile("(?P<label>^PasswordAuthentication\s+)(?P<psswd_auth>[a-z]+)")
        re_x11_forward = re.compile("(?P<label>^X11Forwarding\s+)(?P<x11_forward>[a-z]+)")
        re_use_pam = re.compile("(?P<label>^UsePAM\s+)(?P<use_pam>[a-z]+)")
        
        file_ssh = open(sshd_file)    
        raw_ssh = file_ssh.read()
        file_ssh.close()
        raw_ssh = raw_ssh.split('\n')
        
        for l_ssh in raw_ssh:
            if re_port.match(l_ssh):
                server_to_import.ssh_config.port = re_port.match(l_ssh).group('port')
                server_to_import.ssh_config.results["port"][1] = 1
                count += 1
            if re_protocol.match(l_ssh):
                server_to_import.ssh_config.protocol = re_protocol.match(l_ssh).group('protocol')
                server_to_import.ssh_config.results["protocol"][1] = 1                
                count += 1
            if re_privilege_separation.match(l_ssh):
                server_to_import.ssh_config.use_privilege_separation = re_privilege_separation.match(l_ssh).group('priv_sep')
                server_to_import.ssh_config.results["use_privilege_separation"][1] = 1                
                count += 1
            if re_loglevel.match(l_ssh):
                server_to_import.ssh_config.log_level = re_loglevel.match(l_ssh).group('log_level')
                server_to_import.ssh_config.results["log_level"][1] = 1
                count += 1
            if re_permit_root_login.match(l_ssh):
                server_to_import.ssh_config.permit_root_login = re_permit_root_login.match(l_ssh).group('root_login')
                server_to_import.ssh_config.results["permit_root_login"][1] = 1                
                count += 1
            if re_rsa_auth.match(l_ssh):
                server_to_import.ssh_config.rsa_authentication = re_rsa_auth.match(l_ssh).group('rsa_auth')
                server_to_import.ssh_config.results["rsa_authentication"][1] = 1
                count += 1
            if re_pubkey_auth.match(l_ssh):
                server_to_import.ssh_config.pubkey_authentication = re_pubkey_auth.match(l_ssh).group('pubkey_auth')
                server_to_import.ssh_config.results["pubkey_authentication"][1] = 1
                count += 1
            if re_permit_empty_psswd.match(l_ssh):
                server_to_import.ssh_config.permit_empty_password = re_permit_empty_psswd.match(l_ssh).group('perm_empty_psswd')
                server_to_import.ssh_config.results["permit_empty_password"][1] = 1                
                count += 1
            if re_psswd_auth.match(l_ssh):
                server_to_import.ssh_config.password_authentication = re_psswd_auth.match(l_ssh).group('psswd_auth')
                server_to_import.ssh_config.results["password_authentication"][1] = 1                
                count += 1
            if re_x11_forward.match(l_ssh):
                server_to_import.ssh_config.x11_forwarding = re_x11_forward.match(l_ssh).group('x11_forward')
                server_to_import.ssh_config.results["x11_forwarding"][1] = 1
                count += 1
            if re_use_pam.match(l_ssh):
                server_to_import.ssh_config.use_PAM = re_use_pam.match(l_ssh).group('use_pam')
                server_to_import.ssh_config.results["use_PAM"][1] = 1
                count += 1
                
            # DEFAULT SETTINGS
            # If a param does not match with a regular expression, it is commented or absent.
            # Default param are applied (see sshd_config manual page)
            if server_to_import.ssh_config.port is None:
                server_to_import.ssh_config.port = "22"
                server_to_import.ssh_config.results["port"][1] = 0
            if server_to_import.ssh_config.protocol is None:
                server_to_import.ssh_config.protocol = "2"
                server_to_import.ssh_config.results["protocol"][1] = 0
            if server_to_import.ssh_config.use_privilege_separation is None:
                server_to_import.ssh_config.use_privilege_separation = "yes"
                server_to_import.ssh_config.results["use_privilege_separation"][1] = 0
            if server_to_import.ssh_config.log_level is None:
                server_to_import.ssh_config.log_level = "INFO"
                server_to_import.ssh_config.results["log_level"][1] = 0
            if server_to_import.ssh_config.permit_root_login is None:
                server_to_import.ssh_config.permit_root_login = "yes"
                server_to_import.ssh_config.results["permit_root_login"][1] = 0
            if server_to_import.ssh_config.rsa_authentication is None:
                server_to_import.ssh_config.rsa_authentication = "yes"
                server_to_import.ssh_config.results["rsa_authentication"][1] = 0
            if server_to_import.ssh_config.pubkey_authentication is None:
                server_to_import.ssh_config.pubkey_authentication = "yes"
                server_to_import.ssh_config.results["pubkey_authentication"][1] = 0
            if server_to_import.ssh_config.permit_empty_password is None:
                server_to_import.ssh_config.permit_root_login = "no"
                server_to_import.ssh_config.results["permit_empty_password"][1] = 0
            if server_to_import.ssh_config.password_authentication is None:
                server_to_import.ssh_config.password_authentication = "yes"
                server_to_import.ssh_config.results["password_authentication"][1] = 0
            if server_to_import.ssh_config.x11_forwarding is None:
                server_to_import.ssh_config.x11_forwarding = "no"
                server_to_import.ssh_config.results["x11_forwarding"][1] = 0
            if server_to_import.ssh_config.use_PAM is None:
                server_to_import.ssh_config.use_PAM = "no"
                server_to_import.ssh_config.results["use_PAM"][1] = 0
                
        logger.info(str(count) + " SSH rules imported.")
        
    else:
        logger.warning("Failed importation sshd_config : unable to found a valid file at /etc/ssh/sshd_config location")    


def import_ip_hostname_local(server_to_import, xtract_dir, logger):
    """
    Function which fill the dictionnary ip_hostname with the ip_config result and
    the "hosts" file.
    """
    if server_to_import.interfaces.counter > 0:
        for iface in server_to_import.interfaces.dict.values():
            if iface.ip_adress in server_to_import.ip_hostname_local:
                logger.warning(str(iface.ip_adress) + " ever in the ip_hostname dictionary for the host : " + str(server_to_import.ip_hostname_local[iface.ip_adress]))
            else:
                server_to_import.ip_hostname_local[iface.ip_adress] = server_to_import.name
    else:
        logger.error("No interfaces imported, check that the interfaces import has been well done")
        
    hosts_file = xtract_dir + "/etc/hosts"
    if os.path.isfile(hosts_file):
        f_hosts = open(hosts_file, 'rb')
        rawtext = f_hosts.read()
        f_hosts.close()
        
        rawtext = rawtext.split('\n')
        
        reg_expr = r"(?P<var0>)(?P<ip>^([0-9a-eA-E]*[.:])+[0-9a-eA-E]*)(?P<var1>\s+)(?P<hostname>.*?)(?P<var2>\s+|$)"
        reg_archi = re.compile(reg_expr)
        
        for line in rawtext:
#            print [line]
            result_re = reg_archi.match(line)
            if result_re is not None:
                if str(result_re.group('ip')) in server_to_import.ip_hostname_local:
                    logger.warning(str(result_re.group('ip')) + " ever in the ip_hostname dictionary for the host : " + str(server_to_import.ip_hostname_local[str(result_re.group('ip'))]))
                else:
                    server_to_import.ip_hostname_local[str(result_re.group('ip'))] = str(result_re.group('hostname'))
#                    print str(result_re.group('ip')) + " : " + str(result_re.group('hostname'))
                
        logger.info(str(len(server_to_import.ip_hostname_local)) + " ip_hostname_local imported.")
    else:
        logger.warning("hosts file not found, impossible to import ip_hostname_local")
        
    push_hostname_from_ip_in_connection(server_to_import.connections,server_to_import.ip_hostname_local)
    
def push_hostname_from_ip_in_connection(connections, ip_hostname_local):
    for connection in connections.dict.values():
        if connection.src_ip in ip_hostname_local:
            connection.src_hostname = ip_hostname_local[connection.src_ip]
        if connection.dst_ip in ip_hostname_local:
            connection.dst_hostname = ip_hostname_local[connection.dst_ip]
#    print connections

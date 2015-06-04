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
Created on Wed Jul  2 09:11:16 2014

@author: thierry
"""
import re
import os
import pycaf.architecture.devices.server_features as sf
import pycaf.architecture.devices.server_features.windows as sw
from pycaf.architecture.devices.server_windows import ServerWindows
from pycaf.importer.importServer import Linux
import pycaf.tools as tools

def Import_Windows_server_archive(filename, config):
    """ Create a Server object from an extraction script result archive
    """
    import time

    logger = tools.create_logger(__name__, config)
    
    server_to_import = ServerWindows()

    startTime = time.time()
    
#    [tmp_path, xtract_dir] = Linux.extract_archive(server_to_import, logger, filename)
    [tmp_path, xtract_dir] = extract_archive(logger, filename)
    
    server_to_import.registering_path = config.logs_path
    
    server_to_import.ostype = "Windows Server"
    logger.info("OS type : " + str(server_to_import.ostype))
    import_hostname(server_to_import, xtract_dir, logger)
    logger.info("\nServer hostname : " + str(server_to_import.name))
    
    import_architecture(server_to_import, xtract_dir, logger)
    import_os_name(server_to_import, xtract_dir, logger)
    import_os_and_kernel_version(server_to_import, xtract_dir, logger)
    logger.info("Architecture : " + str(server_to_import.osarchitecture))
    logger.info("OS name : " + str(server_to_import.osname))
    logger.info("OS version : " + str(server_to_import.osversion))
    logger.info("Kernel version : " + str(server_to_import.kernel_version))
    
    import_KB_list(server_to_import, xtract_dir,logger)
    import_interfaces(server_to_import, xtract_dir, logger)
    import_processes(server_to_import, xtract_dir, logger)
    import_connections(server_to_import, xtract_dir, logger)
    import_services(server_to_import, xtract_dir, logger)
    import_software(server_to_import, xtract_dir,logger)
    import_group(server_to_import, xtract_dir,logger)
    import_ip_hostname_local(server_to_import, xtract_dir,logger)

    Linux.remove_extracted_archive(tmp_path, logger)

    endTime = time.time()
    logger.info("Server successfully imported. Time : {0:.2} secs\n".format(endTime - startTime))
    return server_to_import

def extract_archive(logger, filename):
    import zipfile
    import tempfile
    
    tmp_path = None
    
    if os.path.isdir(filename):
        xtract_dir = filename
        hostname = filename.split("/")[-1]
    else:
        # Prepare extraction output directory
        tmp_path = tempfile.mkdtemp()
        
        # 1 - decompress archive
        with zipfile.ZipFile(str(filename), "r") as z:
            z.extractall(tmp_path)
        # Get extraction directory name and server hostname
        for (dirname, dirnames, filenames) in os.walk(tmp_path):
            if len(dirnames) != 1:
                raise zipfile.ExtractError("Unknown archive format")
            hostname = dirnames.pop()
            tmp_xtract_dir = os.path.join(tmp_path, hostname)
            if os.path.isdir(tmp_xtract_dir):
                xtract_dir = tmp_xtract_dir

    return [tmp_path, xtract_dir]
    
def import_hostname(server_to_import, xtract_dir, logger):
    #Import hostname of the windows server contains in the first line of software.txt file
    software_file = xtract_dir + "/software.txt"
    if os.path.isfile(software_file):
        f_soft = open(software_file, 'rb')
        first_line = f_soft.readline()
        f_soft.close()
        
        reg_expr = r"(?P<var1>.*?\\\\)(?P<hostname>.*?)(?P<var2>:)"
        reg_hostname = re.compile(reg_expr)
        result_re = reg_hostname.match(first_line)
        if result_re is not None:
            server_to_import.name = result_re.group('hostname')
        else:
            logger.error("Unable to find the hostname in the first line of software.txt")
            exit(1)
    else:
        logger.error("Hostname import error : software.txt file not found")
        exit(1)
         
def import_architecture(server_to_import, xtract_dir, logger):
      server_to_import.osarchitecture = get_architecture(xtract_dir,logger)

def import_os_name(server_to_import, xtract_dir, logger):
    """
    Import os windows pretty name as defined at :
    https://technet.microsoft.com/fr-fr/security/bulletin
    """
    
    # Import the year and R2
    system_file = xtract_dir + "/system_info.txt"
    if os.path.isfile(system_file):
        f_system = open(system_file, 'rb')
        rawtext = f_system.read()
        f_system.close()
        
        rawtext = rawtext.split('\n')
        reg_year_expr = r"(?P<prev>.*?)(?P<year>20[0-9]{2})"
        
        year = None
        architecture = None
        R2 = None
        SP = None
        server_core = ''
        
        for line in rawtext:
            # Line containing the name
            if "Windows" in line and "Server" in line:
                result_re = re.match(reg_year_expr, line)
                if result_re is not None:
                    year = result_re.group('year')
                if "R1" in line:
                    R2 = "R1"
                elif "R2" in line :
                    R2 = "R2"
                else:
                    R2 = ''
            
            if "ersion" in line and ("OS" in  line or "syst" in line) and "BIOS" not in line:
                if "Service Pack 1" in line:
                    SP = "Service Pack 1"
                elif "Service Pack 2" in line:
                    SP = "Service Pack 2"
                else:
                    SP = ''   
                    
            if R2 is not None and SP is not None:
                break
    else:
        logger.error("OS windows name import error : system_info.txt file not found")
        exit(1)
    # Import architecture
    architecture = get_architecture(xtract_dir,logger)
    if not architecture:
        logger.error("OS windows architecture import error")
        exit(1)
        
    if (year and architecture and SP and R2 and server_core) is not None:
        os_name = get_os_pretty_name(year, architecture, SP, R2, server_core)
        
        if not os_name:
            logger.error("OS windows name import error")
        else:
            server_to_import.osname = os_name
    else:
        logger.error("OS windows name import error")
   
def import_os_and_kernel_version(server_to_import, xtract_dir, logger):
    # Import the year and R2
    system_file = xtract_dir + "/hotfixes.txt"
    if os.path.isfile(system_file):
        f_system = open(system_file, 'rb')
        rawtext = f_system.read()
        f_system.close()
        
        rawtext = rawtext.split('\n')
        reg_kernel_version_expr = r"(?P<prev>.*?Kernel build number.*?)(?P<kernel>[0-9.]+)"
        reg_os_version_expr = r"(?P<prev>.*?Product version.*?)(?P<os_version>[0-9.]+)"
        
        for line in rawtext:
            # Line containing the kernel version
            if "Kernel build number" in line:
                result_re = re.match(reg_kernel_version_expr, line)
                if result_re is not None:
                    kernel_version = result_re.group('kernel')
                    server_to_import.kernel_version = kernel_version
                else:
                    logger.warning("Unable to import  the kernel version")
            if "Product version" in line:
                result_re = re.match(reg_os_version_expr, line)
                if result_re is not None:
                    os_version = result_re.group('os_version')
                    server_to_import.osversion = os_version
                else:
                    logger.warning("Unable to import  the kernel version")
        if server_to_import.osversion is None:
            logger.warning("OS version not imported")
        if server_to_import.kernel_version is None:
            logger.warning("Kernel version not imported")
            
                    
    else:
        logger.error("OS version and kernel import error : hotfixes.txt file not found")
                    
#def import_KB_list(server_to_import, xtract_dir, logger):
    
    
def import_interfaces(server_to_import, xtract_dir, logger):
    # Importation of windows server interfaces
    interface_file = xtract_dir + "/ipconfig.txt"

    
    if os.path.isfile(interface_file):    
        server_to_import.interfaces = sf.InterfaceList()
        f_interface = open(interface_file, 'rb')
        raw_interface_file = f_interface.read()
        f_interface.close()
        
        blocks_interface = raw_interface_file.split('Ethernet')
        
        #Supress the first case which is useless
        blocks_interface = blocks_interface[1:]
        
        iface_reg_expr_name = r"(?P<previous>^.*?Description.*?: )(?P<name>.*?)(?P<post>\r)"
        iface_reg_expr_mac = r"(?P<previous>^.*?(p|P)hysi.*?: )(?P<mac>([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2})"
        iface_reg_expr_ipv4 = r"(?P<previous>^.*?IP(v4)* Address.*?: )(?P<ipv4>([0-9]+.){3}([0-9]+){1})"
        iface_reg_expr_ipv6 = r"(?P<previous>^.*?IPv6.*?: )(?P<ipv6>[0-9a-fA-F:%]+)"
        iface_reg_expr_mask = r"(?P<previous>^.*?Mas(k|que).*?: )(?P<mask>([0-9]+.){3}([0-9]+){1})"
    
        reg_iface_name = re.compile(iface_reg_expr_name)
        reg_iface_mac = re.compile(iface_reg_expr_mac)
        reg_iface_ipv4 = re.compile(iface_reg_expr_ipv4)
        reg_iface_ipv6 = re.compile(iface_reg_expr_ipv6)
        reg_iface_mask = re.compile(iface_reg_expr_mask)
        
        for l_iface in blocks_interface:
            interface = sf.Interface()
            lines_iface = l_iface.split('\n')

            import_results = {'name' : False, 'mac' : False, 'ipv4' : False, 'mask' : False}
            import_ipv6 = False            
            for line_interface in lines_iface:
                # Import interface name
                if (reg_iface_name.match(line_interface) is not None and import_results['name'] is False):
                    result_re = reg_iface_name.match(line_interface)
                    interface.name = result_re.group('name')
                    import_results['name'] = True
                if (reg_iface_mac.match(line_interface) is not None and import_results['mac'] is False):
                    result_re = reg_iface_mac.match(line_interface)
                    interface.mac = result_re.group('mac')
                    import_results['mac'] = True
                if (reg_iface_ipv4.match(line_interface) is not None and import_results['ipv4'] is False):
                    result_re = reg_iface_ipv4.match(line_interface)
                    interface.ip_adress = result_re.group('ipv4')
                    import_results['ipv4'] = True
                if (reg_iface_ipv6.match(line_interface) is not None and import_ipv6 is False):
                    result_re = reg_iface_ipv6.match(line_interface)
                    interface.ipv6_address = result_re.group('ipv6')
                    import_ipv6 = True
                if (reg_iface_mask.match(line_interface) is not None and import_results['mask'] is False):
                    result_re = reg_iface_mask.match(line_interface)
                    interface.mask = result_re.group('mask')
                    import_results['mask'] = True
                    
            if False in import_results.values():
                logger.warning(str(import_results))
                logger.warning("Unable to import a Microsoft Windows interface")
            else:
                server_to_import.interfaces.add_interface(interface)
            if import_ipv6 is True:
                logger.debug("IPv6 address imported")
                
        logger.info(str(server_to_import.interfaces.counter) + " interfaces imported.")
    else:
        logger.warning("Failed importation /ipconfig.txt : unable to found a valid file")
        
def import_connections(server_to_import, xtract_dir, logger):
    # Import connection
    connection_file = xtract_dir + "/netstat.txt"
    
    if len(server_to_import.pid_name_dict) == 0:
        logger.warning("Import processes before connections in order to have the program name corresponding to the PID")
    
    if os.path.isfile(connection_file):
        server_to_import.connections = sf.ConnectionList()
        f_netstat = open(connection_file, 'rb')
        raw_connection_file = f_netstat.read()
        f_netstat.close()
        
        lines_connection = raw_connection_file.split('\n')

        connection_ext_expression = (r"(?P<space1>^\s*)(?P<proto>\w+)(?P<space2>\s+)"
        r"(?P<ip_src>(([0-9]+.){3}([0-9]+){1})|\[[0-9a-fA-F:%]+\])"
        "(?P<colonn1>:)(?P<port_src>[0-9]+)(?P<space3>\s+)"
        r"(?P<ip_dst>(([0-9]+.){3}([0-9]+){1})|\[[0-9a-fA-F:%]+\]|\*)"
        r"(?P<colonn2>:)(?P<port_dst>([0-9]+)|\*)"
        r"(?P<space4>\s+)(?P<state>[A-Z_]*)(?P<space5>\s+)(?P<pid>[0-9]+)")        
        
        connection_reg_ext = re.compile(connection_ext_expression)
        
        for l_connection in lines_connection:
            if (connection_reg_ext.match(l_connection) is not None):
                result_re = connection_reg_ext.match(l_connection)
                pid = str(result_re.group('pid'))
                if len(server_to_import.pid_name_dict) > 0 and pid in server_to_import.pid_name_dict.keys():
                    prog_name = server_to_import.pid_name_dict[pid]
                else:
                    prog_name = None
                server_to_import.connections.add_connection(sf.Connection(result_re.group('proto'),\
                result_re.group('ip_src'), result_re.group('port_src'), result_re.group('ip_dst'),\
                result_re.group('port_dst'), result_re.group('state'), result_re.group('pid'), prog_name))

        logger.info(str(server_to_import.connections.counter) + " connections imported.")
    else:
        logger.warning("Failed importation /netstat.txt configuration : unable to found a valid file")
       
def import_processes(server_to_import, xtract_dir, logger):
    # Import processes with the file ps2.txt
    ps_file = xtract_dir + "/ps2.txt"
    
    if os.path.isfile(ps_file):    
        server_to_import.processes = sw.ProcessWindowsList()
        f_ps = open(ps_file, 'rb')
        raw_ps_file = f_ps.read()
        f_ps.close()
        
        lines_ps = raw_ps_file.split('\n')
        
        ps_reg_expression = (r"(?P<name>^([A-Za-z0-9_.]|( [\w]))+)(?P<space1>\s+)(?P<pid>[0-9]+)"
        r"(?P<space2>\s+)(?P<session_name>[a-zA-Z0-9#_\-]*)(?P<space3>\s+)(?P<session>[0-9]+)"
        r"(?P<space4>\s+)(?P<useless_info>.*? .*? .*?\s+)(?P<username>([A-Za-z0-9_\\/.]|( [\w]))+)")
       
        ps_reg = re.compile(ps_reg_expression)
        
        for l_ps in lines_ps:
            if (ps_reg.match(l_ps) is not None):
                result_re = ps_reg.match(l_ps)
                server_to_import.pid_name_dict[str(result_re.group('pid'))] = str(result_re.group('name'))                
                server_to_import.processes.add_process(sw.ProcessWindows(result_re.group('pid'),\
                result_re.group('name'), result_re.group('username'), result_re.group('session_name')))
        logger.info(str(server_to_import.processes.counter) + " processes imported.")
    else:
        logger.warning("Failed importation /ps-format.txt : unable to found a valid file")

def import_KB_list(server_to_import, xtract_dir,logger):
    patch_file = xtract_dir + "/installed_patches.txt"
    if os.path.isfile(patch_file):
        server_to_import.kb_patches = sw.KBpatchList()
        f_patch = open(patch_file, 'rb')
        rawtext = f_patch.read().decode('utf-16')
        f_patch.close()
        rawtext = rawtext.split('\n')
        
        reg_KB_expr = r"(?P<var1>.*?KB)(?P<KB>[0-9]+)"
        
        for line in rawtext:
            result_re = re.match(reg_KB_expr, line)
            if result_re is not None:
                KB = int(result_re.group('KB'))
                server_to_import.kb_patches.add_kb(sw.KBpatch(KB))
        logger.info(str(server_to_import.kb_patches.counter) + " KB imported.")
        
    else:
        logger.error("KB list import error : installed_patches.txt file not found")
        return False
       
def import_services(server_to_import, xtract_dir,logger):
    service_file = xtract_dir + "/services.txt"
    if os.path.isfile(service_file):
        server_to_import.services = sw.ServiceWindowsList()
        f_service = open(service_file, 'rb')
        rawtext = f_service.readlines()
        f_service.close()
        
        for line in rawtext:
            params = line.split(',')
            for i, prm in enumerate(params):
                params[i] = prm.strip()
            if len(params) == 6:
                server_to_import.services.add_service(sw.ServiceWindows(params[1], params[2], params[3], params[4]))
        logger.info(str(server_to_import.services.counter) + " services imported.")
        
    else:
        logger.error("Services list import error : services.txt file not found")
        return False
        
def import_software(server_to_import, xtract_dir,logger):
    soft_file = xtract_dir + "/software.txt"
    server_to_import.software = sw.SoftwareWindowsList()
    if os.path.isfile(soft_file):
        f_soft = open(soft_file, 'rb')
        rawtext = f_soft.read().split('\r\n')
        f_soft.close()
        
        register_soft = False
        for line in rawtext:
            if "Applications:" in line:
                register_soft = True
            elif register_soft and line != '':
                server_to_import.software.add_software(line)
        
        if not register_soft:
            logger.error("Sofware importation error")
        else:
            logger.info(str(server_to_import.software.counter) + " software imported.")
                
    else:
        logger.error("KB list import error : installed_patches.txt file not found")
        return False
        
def import_group(server_to_import, xtract_dir,logger):
    group_file = xtract_dir + "/u_groups.txt"
    server_to_import.groups = sw.GroupWindowsList()
    if os.path.isfile(group_file):
        f_group = open(group_file, 'rb')
        rawtext = f_group.read().split('\r\n')
        f_group.close()

        for line in rawtext:
            list_param = line.split(',')
            # A group line contain 5 parameters : Group,Comment,GroupType,GroupMember,MemberType
            if len(list_param) == 5:
                group = list_param[0]
                comment = list_param[1]
                grouptype = list_param[2]
                groupmember = list_param[3]
                membertype = list_param[4]
                grp_to_add = sw.GroupWindows(group, grouptype, groupmember, membertype, comment)
                server_to_import.groups.add_group(grp_to_add)

        else:
            logger.info(str(server_to_import.groups.counter) + " groups imported.")
                
    else:
        logger.error("Group list import error : u_groups.txt file not found")
        return False
        
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
        
    hosts_file = xtract_dir + "/hosts"
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
                    logger.warning(str(result_re.group('ip')) + " ever in the ip_hostname dictionary for the host : " + str(server_to_import.ip_hostname_local[iface.ip_adress]))
                else:
                    server_to_import.ip_hostname_local[str(result_re.group('ip'))] = str(result_re.group('hostname'))
#                    print str(result_re.group('ip')) + " : " + str(result_re.group('hostname'))
                
        logger.info(str(len(server_to_import.ip_hostname_local)) + " ip_hostname_local imported.")
    else:
        logger.warning("hosts file not found, impossible to import ip_hostname_local")
    
    push_hostname_from_ip_in_connection(server_to_import.connections,server_to_import.ip_hostname_local)
        
def get_architecture(xtract_dir,logger):
    #Import architecture of the windows server (x64,Itanium,...) contains in the system_info.txt file
    system_file = xtract_dir + "/system_info.txt"
    if os.path.isfile(system_file):
        f_system = open(system_file, 'rb')
        rawtext = f_system.read()
        f_system.close()
        
        rawtext = rawtext.split('\n')
        
        reg_expr = r"(?P<var1>.*?:\s+)(?P<archi>.*?)(?P<var2>\s+)"
        reg_archi = re.compile(reg_expr)
        
        for line in rawtext:
            if (("Syst" or "syst") in line) and (("Type" or "type") in line):
                result_re = reg_archi.match(line)
                if result_re is not None:
                    arch = result_re.group('archi')
                    if "x64" in arch:
                        return "x64"
                    elif "X86" in arch:
                        return "32-bit"
                    elif "Itanium" in arch:
                        return "Itanium"
                    else:
                        logger.warning("Windows architecture unknown") 
                        return False
            
        logger.error("Architecture import error : unable to determine it")
        return False
    else:
        logger.error("Architecture import error : system_info.txt file not found")
        return False
        
def get_os_pretty_name(annee, architecture, SP, R2, server_core_install):
    """
    Get parameters to determine the pretty name of the OS.
    The full list of OS are available in the ressource folder
    """
    import ressources.analyzer.server as ressources
    config_server = ressources.ConfigServer(4)
    windows_os_list = config_server.windows['os_list']
    
    if annee == '2003' and architecture == '32-bit':
        architecture = ['x64', 'Itanium']
    elif annee == '2012' and architecture == 'x64':
        architecture = ['32-bit', 'Itanium']
    if SP == '':
        SP = ['Service Pack 1', 'Service Pack 2']
    if R2 == '':
        R2 = ['R1', 'R2']
    if server_core_install == '':
        server_core_install = ['Server Core installation']
        
    filter_list = [annee, architecture, SP, R2, server_core_install]
    
    for os_version in windows_os_list:
        match = True
        for filt in filter_list:
            if isinstance(filt, list):
                for elem_to_avoid in filt:
                    if elem_to_avoid.lower() in os_version.lower():
                        match = False
            elif filt.lower() not in os_version.lower():
                match = False
        if match:
            return os_version
    return False
    
def push_hostname_from_ip_in_connection(connections, ip_hostname_local):
    for connection in connections.dict.values():
        if connection.src_ip in ip_hostname_local:
            connection.src_hostname = ip_hostname_local[connection.src_ip]
        if connection.dst_ip in ip_hostname_local:
            connection.dst_hostname = ip_hostname_local[connection.dst_ip]
#    print connections

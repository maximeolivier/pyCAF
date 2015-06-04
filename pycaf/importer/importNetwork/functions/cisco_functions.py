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
Created on Fri Aug  1 17:13:56 2014

@author: thierry
"""
import re
import pycaf.architecture.devices.network_features as nf






#def Import_cisco_switch_file(filename, config):
#    """ Create a Server object from an extraction script result archive
#    """
#    import time
#
#    logger = tools.create_logger(__name__, config)
#    
#    switch_to_import = Switch()
#
#    startTime = time.time()
#    
#
#    if not os.path.isfile(filename):
#        logger.error("Cisco switch import error, file not foud : " + str(filename))
#        return False
#    else:
#        switch_to_import.name = filename.split('/')[-1]
#        switch_to_import.manufacturer = "Cisco"
#        
##        Open the file and store lines in a list
#        file_switch = open(filename, 'rb')
#        file_content_lines = file_switch.readlines()
#        file_switch.seek(0, 0)
#        file_content_exclamation = file_switch.read().split('!\n')
#        file_switch.close()
#        
#        import_hostname(switch_to_import, file_content_lines, logger)
#        import_osversion(switch_to_import, file_content_lines, logger)
#        import_vlan(switch_to_import, file_content_exclamation, logger)
#        import_interfaces_and_switchport(switch_to_import, file_content_exclamation, logger)
#        import_route(switch_to_import, file_content_lines, logger)
#        
#        print switch_to_import
#        print switch_to_import.vlan
#        print switch_to_import.interfaces
#        print switch_to_import.switchport
#        print switch_to_import.routes
#    
##        import_osname(server_to_import, xtract_dir, logger)
#    
#        endTime = time.time()
#        logger.info("Cisco switch successfully imported. Time : {0:.2} secs\n".format(endTime - startTime))
#    return switch_to_import
       
def import_cisco_hostname(switch_to_import, file_content, logger):
    if len(file_content) < 1:
        logger.error("File content empty")
    else:
        hostname_expression = r"(?P<label>^hostname\s+)(?P<hostname>.*?)(?P<endline>\s+)"
        hostname_reg = re.compile(hostname_expression)
        
        for line in file_content:
            reg_resullt = hostname_reg.match(line)
            if reg_resullt is not None:
                switch_to_import.hostname = reg_resullt.group('hostname')
                break
        if switch_to_import.hostname is None:
            logger.error("Failed to import hostname")
            
def import_cisco_osversion(switch_to_import, file_content, logger):
    if len(file_content) < 1:
        logger.error("File content empty")
    else:
        version_expression = r"(?P<label>^version\s+)(?P<version>.*?)(?P<endline>\s+)"
        version_reg = re.compile(version_expression)
        
        for line in file_content:
            reg_resullt = version_reg.match(line)
            if reg_resullt is not None:
                switch_to_import.osversion = reg_resullt.group('version')
                break
        if switch_to_import.hostname is None:
            logger.error("Failed to import osversion")
            
def import_cisco_vlan(switch_to_import, file_content, logger):
    if len(file_content) < 1:
        logger.error("File content empty")
    else:
        vlan_expression = r"(?P<label>^vlan\s+)(?P<vlan_nb>[0-9]+)(?P<label2>\s+name\s+)(?P<name>.*?)(?P<endline>\s+)"
        vlan_reg = re.compile(vlan_expression)
        
        for elem in file_content:
            if elem.startswith("vlan"):
                reg_result = vlan_reg.match(elem)
                if reg_result is not None:
                    new_vlan = nf.Vlan()
                    new_vlan.number = reg_result.group('vlan_nb')
                    new_vlan.name = reg_result.group('name')
                    switch_to_import.vlan.add_vlan(new_vlan)
                else:
                    logger.debug("vlan line mismatching : " + str(elem))
                
            
        if switch_to_import.vlan.counter > 0:
            logger.info(str(switch_to_import.vlan.counter) + " vlan imported")
            
def import_cisco_interfaces_and_switchport(switch_to_import, file_content, logger):
    if len(file_content) < 1:
        logger.error("File content empty")
    else:
        interface_expression = r"(?P<label>^interface\s+)(?P<name>.*?)(?P<endline>\s+)"
        interface_ip_expression = r"(?P<label>\s*ip address\s+)(?P<addr_ip>.*?)(?P<separator>\s+)(?P<mask>.*?)(?P<endline>\s*$)"
        iface_access_group_expression = r"(?P<label>\s*ip access-group\s+)(?P<name>.*?)(?P<separator>\s+)(?P<direction>.*?)(?P<endline>\s*$)"
        
        description_expression = r"(?P<label>\s*description\s+)(?P<descr>.*?)(?P<endline>$)"

        switchport_mode_expr = r"(?P<label>\s*switchport mode\s+)(?P<mode>.*?)(?P<endline>\s*$)"
        switchport_vlan_expr = r"(?P<label>\s*switchport (access|trunk native) vlan\s+)(?P<vlan>[0-9]+)(?P<endline>\s*$)"
        switchport_trunk_allowed_expr = r"(?P<label>\s*switchport trunk allowed vlan\s+)(?P<vlan>.*?)(?P<endline>\s*$)"
        
        inferface_reg = re.compile(interface_expression)
        interface_ip_reg = re.compile(interface_ip_expression)
        iface_access_group_reg = re.compile(iface_access_group_expression)
        description_reg = re.compile(description_expression)
        switchport_mode_reg = re.compile(switchport_mode_expr)
        switch_vlan_reg = re.compile(switchport_vlan_expr)
        switchport_trunk_allowed_reg = re.compile(switchport_trunk_allowed_expr)
                
        for elem in file_content:
            if elem.startswith("interface"):
                iface_reg_result = inferface_reg.match(elem)
                if iface_reg_result is not None:
                    new_interface = nf.Interface()
                    new_switchport = nf.Switchport()
                    new_interface.name = iface_reg_result.group('name')
                    new_switchport.interface = iface_reg_result.group('name')

                    if "shutdown" in elem:
                        new_interface.active = "no"
                    else:
                        new_interface.active = "yes"
                        
                    lines_elem = elem.split('\n')
                    for line_elem in lines_elem:
                        descr_reg_result = description_reg.match(line_elem)
                        iface_ip_reg_result = interface_ip_reg.match(line_elem)
                        iface_access_group_res = iface_access_group_reg.match(line_elem)
                        switch_mode_reg_result = switchport_mode_reg.match(line_elem)
                        switch_vlan_reg_result = switch_vlan_reg.match(line_elem)
                        switch_trunk_allowed_reg_result = switchport_trunk_allowed_reg.match(line_elem)
                        
                        if descr_reg_result is not None:
                            new_interface.description = descr_reg_result.group('descr')
                            new_switchport.description = descr_reg_result.group('descr')
                        if iface_ip_reg_result is not None:
                            new_interface.ip = iface_ip_reg_result.group('addr_ip')
                            new_interface.mask = iface_ip_reg_result.group('mask')
                        if iface_access_group_res is not None:
                            if "in" in iface_access_group_res.group('direction').lower():
                                new_interface.acl_list_in = iface_access_group_res.group('name')
                            elif "out" in iface_access_group_res.group('direction').lower():
                                new_interface.acl_list_out = iface_access_group_res.group('name')
                            else:
                                logger.warning("access group direction unfound : " + str(elem))
                        if switch_mode_reg_result is not None:
                            new_switchport.mode = switch_mode_reg_result.group('mode')
                        if switch_vlan_reg_result is not None:
                            new_switchport.vlan = switch_vlan_reg_result.group('vlan')
                        if switch_trunk_allowed_reg_result is not None:
                            rawdata = switch_trunk_allowed_reg_result.group('vlan')
                            rawdata = rawdata.split(',')
                            for data in rawdata:
                                vlan_number = int(data.strip())
                                new_switchport.vlan_allowed.append(vlan_number)
                                
                    switch_to_import.interfaces.add_interface(new_interface)
                    switch_to_import.switchport.add_switchport(new_switchport)
                else:
                    logger.debug("interface line mismatching : " + str(elem))
                
            
        if switch_to_import.interfaces.counter > 0:
            logger.info(str(switch_to_import.interfaces.counter) + " interfaces imported")
            
def import_cisco_route(switch_to_import, file_content, logger):
    if len(file_content) < 1:
        logger.error("File content empty")
    else:
        route_expression = r"(?P<label>^ip route\s+)(?P<dst>.*?)(?P<sep1>\s+)(?P<mask>.*?)(?P<sep2>\s+)(?P<interface>.*?)(?P<endline>\s+.*?$)"
        route_reg = re.compile(route_expression)
        
        for elem in file_content:
            if elem.startswith("ip route"):
                reg_result = route_reg.match(elem)
                if reg_result is not None:
                    new_route = nf.Route()
                    new_route.destination = reg_result.group('dst')
                    new_route.mask = reg_result.group('mask')
                    new_route.interface = reg_result.group('interface')
                    switch_to_import.routes.add_route(new_route)
                else:
                    logger.debug("ip route line mismatching : " + str(elem))
                
            
        if switch_to_import.routes.counter > 0:
            logger.info(str(switch_to_import.routes.counter) + " routes imported")
    
def import_cisco_catalyst_acl_table(switch_to_import, file_content, logger):
    if len(file_content) < 1:
        logger.error("File content empty")
    else:
        acl_name_expression = r"(?P<label>^ip access-list\s+)(?P<type>.*?)(?P<sep>\s+)(?P<name>.*?)(?P<endline>\s*$)"
        acl_name_reg = re.compile(acl_name_expression)
        
        # example : permit udp 10.0.16.0 0.0.15.255 host 10.0.5.2 eq tftp
        # regex     filter proto src_ip  mask       dst_ip mask   facultative keyword
        # if (src|dst)_ip == host : (src|dst)_ip = mask
        # facultatives words : eq x, neq x, range x y, gt x, lt x
        extended_expr = (r"(?P<start>^ )(?P<filter>.*?)(?P<sep1>\s+)(?P<proto>.*?)(?P<sep2>\s+)"
        r"(?P<src_ip>.*?)(?P<sep3>\s+)(?P<src_mask>.*?)(?P<sep4>\s+)(?P<src_port_eq>(eq .*? )*)(?P<src_port_neq>(neq .*?)*)"
        r"(?P<src_port_gt>(gt .*?)*)(?P<src_port_lt>(lt .*?)*)(?P<src_port_range>(range .*? .*?)*)"
        r"(?P<dst_ip>.*?)(?P<sep5>\s+)(?P<dst_mask>.*?)(?P<sep6>\s*)(?P<dst_port_eq>(eq .*?)*)(?P<dst_port_neq>(neq .*?)*)"
        r"(?P<dst_port_gt>(gt .*?)*)(?P<dst_port_lt>(lt .*?)*)(?P<dst_port_range>(range .*? .*?)*)(?P<end_line>\s+.*)")
        extended_reg = re.compile(extended_expr)
        
        fill_acl = False    # Boolean value to fill the ACL list
        remark = None
        
        for line in file_content:
            # Start of an ACL list
            if line.startswith("ip access-list"):
                if fill_acl:
                    switch_to_import.acl_table.add_acl_list(acl_list_name, new_acl_list)
                    fill_acl = False
                
                result_re = acl_name_reg.match(line)
                if result_re is not None:
                    acl_type = 0
                    acl_list_name = result_re.group('name')
                    
                    acl_type_str = result_re.group('type')
                    if acl_type_str.lower() == "standard":
                        acl_type = 1
                    elif acl_type_str.lower() == "extended":
                        acl_type = 2
                    else:
                        acl_type = 0
                        
                    new_acl_list = nf.ACLlist()
                    fill_acl = True
            # Continue to fill an ACL
            elif line.startswith(" ") and fill_acl:
#                print "jello"
                if acl_type == 2:
                    result_re = extended_reg.match(line)
                    if result_re is not None:
#                        print line
                        
                        filter_acl = result_re.group('filter')
                        if filter_acl == "permit" or filter_acl == "deny":
                            new_acl = nf.ACL()
                            new_acl.type = 2
                            new_acl.filter = filter_acl
                            new_acl.protocol = result_re.group('proto')
                            if result_re.group('src_ip') == "host":
                                new_acl.src_ip = result_re.group('src_mask')
                            else:
                                new_acl.src_ip = result_re.group('src_ip')
                                new_acl.src_mask = result_re.group('src_mask')
                                
                            if result_re.group('dst_ip') == "host":
                                new_acl.dst_ip = result_re.group('dst_mask')
                            else:
                                new_acl.dst_ip = result_re.group('dst_ip')
                                new_acl.dst_mask = result_re.group('dst_mask')
                            
                            if result_re.group('dst_port_eq') != "":
                                new_acl.dst_port = result_re.group('dst_port_eq').strip()[3:]
                            elif result_re.group('dst_port_neq') != "":
                                new_acl.dst_port = result_re.group('dst_port_neq').strip()
                            elif result_re.group('dst_port_gt') != "":
                                new_acl.dst_port = "> " + str(result_re.group('dst_port_gt').strip()[3:])
                            elif result_re.group('dst_port_lt') != "":
                                new_acl.dst_port = "< " + str(result_re.group('dst_port_lt').strip()[3:])
                            elif result_re.group('dst_port_range') != "":
                                new_acl.dst_port = result_re.group('dst_port_range').strip()
                                
                            if result_re.group('src_port_eq') != "":
                                new_acl.src_port = result_re.group('src_port_eq').strip()[3:]
                            elif result_re.group('src_port_neq') != "":
                                new_acl.src_port = result_re.group('src_port_neq').strip()
                            elif result_re.group('src_port_gt') != "":
                                new_acl.src_port = "> " + str(result_re.group('src_port_gt').strip()[3:])
                            elif result_re.group('src_port_lt') != "":
                                new_acl.src_port = "< " + str(result_re.group('src_port_lt').strip()[3:])
                            elif result_re.group('src_port_range') != "":
                                new_acl.src_port = result_re.group('src_port_range').strip()
                                
                            
                            if remark is not None:
                                new_acl.comment = remark
                                remark = None
                            new_acl_list.add_acl(new_acl)
                        elif filter_acl == "remark":
                            remark = line.strip()
            # ACL list is filling and it is the end of the ACL list
            elif fill_acl:
                switch_to_import.acl_table.add_acl_list(acl_list_name, new_acl_list)
                fill_acl = False

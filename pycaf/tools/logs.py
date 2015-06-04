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
Logs management
"""
import logging
import os

tmp_dir_name = "tmp_logs/"
global main_logger
main_logger = None


def create_logger(name, config, is_main=False):
    """
    Function wich create a logger with settings in config file
    """
    # Get if exist the main logger
    global main_logger

    # Get previous logger
    logger = logging.getLogger(name)

    # If the logger was not previously initialized (no handlers)
    if not logger.handlers:
        path = config.logs_path

        if not is_main:
            path += tmp_dir_name

        if not os.path.exists(path):
            os.makedirs(path)

        level_str = config.logs_level.lower()
        if level_str == "debug":
            level = logging.DEBUG
        elif level_str == "info":
            level = logging.INFO
        elif level_str == "warning":
            level = logging.WARNING
        elif level_str == "error":
            level = logging.ERROR
        elif level_str == "critical":
            level = logging.CRITICAL

        logger.setLevel(level)

        # Set the log file name stored into de conf file
        if not is_main:
            path += name
        else:
            path += config.logs_file_name

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        hdlr = logging.FileHandler(path, mode='w')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(level)
        logger.addHandler(steam_handler)

        if is_main:
            main_logger = logger
            logger.debug("Main logger : " + str(path))
            logger.debug("Temp logs path at : " + str(config.logs_path + tmp_dir_name))

        elif not is_main and (main_logger is not None):
            main_logger.debug("New logger : " + str(name) + " - path : " + str(path))

    return logger


def merge_logs(config):
    """
    Merge log files in a unique file and delete the others.
    Function may called when all analyze threads are terminated.
    """
    path_file_logs = config.logs_path + config.logs_file_name
    path_tmp = config.logs_path + tmp_dir_name

    if not os.path.exists(path_tmp) or main_logger is None:
        return False
    else:
        f_main_log = open(path_file_logs, 'ab')

        for tmp_log in os.listdir(path_tmp):
            path_tmp_log = path_tmp + tmp_log
            f_tmp = open(path_tmp_log, 'rb')
            data = f_tmp.read()
            f_tmp.close()
            f_main_log.write(data)
            os.remove(path_tmp_log)

        f_main_log.close()

        # If the tmp_logs directory is empty, it deletes it.
        if not os.listdir(path_tmp):
            os.removedirs(path_tmp)

        return True

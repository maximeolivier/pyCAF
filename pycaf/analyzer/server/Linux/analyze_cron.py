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
Created on Wed May 28 15:25:05 2014

@author: thierry
"""
import threading
import time
import pycaf.tools as tools
import pycaf.architecture.devices.server_features as sf
import re


class AnalyzeCron (threading.Thread):
    """Check the rights of files executed with crontab
    """

    def __init__(self, server, config):
        threading.Thread.__init__(self)

        self.server = server
        self.config = config
        self._logger = tools.create_logger(__name__, self.config)

    def run(self):
        self._logger.info("Run crontab checking")

        if self.check_ressources():
            self.analyze()
#            if self.check_results():
#                self.log_results()
#            else:
#                self._logger.error("AnalyzeDebianCron Error")
        else:
            self._logger.error("AnalyzeDebianCron Error")

    def analyze(self):
        """
        Core function which is called in the run
        Do the effective work
        """
        start_time = time.time()

        # Check crontab algorithm
        # Step 1 : Split lines and extract files path
        # Ok -> Step 2    KO -> Unable to determine an executed file
        # Step 2 : check if path match with de files list imported
        # Ok -> Step 3    KO -> Unable to determine an executed file
        # Step 3 : Pick up rights and determine if they are safe
        # Ok -> No threat detected    KO -> Privilege escalation threat

#        file_path_expression = r"(?P<var1>(.+?){5}.*?)(?P<path>/((\\ )|(?!\s).)*)"
        file_path_expression = r"(?P<var1>.*?)(?P<path>/((\\ )|(?!\s).)*)"
        file_path_reg = re.compile(file_path_expression)

        for user in self.server.crontab_config.keys():
            # --------------------------------------------
            # ------------------ Step 1 ------------------
            # --------------------------------------------
            raw_lines = self.server.crontab_config[user].split(' /')

            for i, l_cron in enumerate(raw_lines):
                # Add a '/' removed by the split method except the first string in the list
                if i != 0:
                    l_cron = "/" + str(l_cron)
                if file_path_reg.match(l_cron) is not None:
                    result_re = file_path_reg.match(l_cron)
                    path_name = result_re.group('path')

                    # --------------------------------------------
                    # ------------------ Step 2 ------------------
                    # --------------------------------------------
                    file_database = self.server.files.filter_files(path = str(path_name))

                    if file_database.counter == 1:
                        # ------------------ Step 3 ------------------
                        file_to_check = file_database.get_file(1)
                        if tools.compare_rights(file_to_check.rights, "*****-**-*"):
                            tmp_str = "{:<20} {:<40} {:<15}".format(str(user), str(file_to_check.path), "no threat")
                            self.server.crontab_results.append(tmp_str)
                        else:
                            tmp_str = "{:<20} {:<40} {:<15}".format(str(user), str(file_to_check.path), "privilege escalation threat")
                            self.server.crontab_results.append(tmp_str)
                    else:
                        tmp_str = "{:<20} {:<40} {:<15}".format(str(user), str(path_name), "file not found in the imported list")
                        self.server.crontab_results.append(tmp_str)

        end_time = time.time()
        self._logger.info("Debian crontab configuration successfully analyzed.")
        self._logger.info("Elapsed time: {0:.2} secs".format(end_time - start_time))

        return True

    def check_ressources(self):
        """
        Check ressources before processing the analyze
        """
        # Check that dictionnary of crontab is not empty
        if len(self.server.crontab_config) == 0:
            self._logger.error("Empty crontab configuration dictionnary : check your importation")
            return False
        elif self.server.files.counter == 0:
            self._logger.error("Empty files list : check your importation")
            return False
        else:
            self._logger.debug("Ressources well checked for crontab analysis")
            return True

    def check_results(self):
        """
        Check results after analyze in order to detect analysis error
        For example : number of files is not coherent
        """
        if -1 in self.server.ssh_config.results:
            self._logger.warning("All SSH parametrers not checked !")
            return False
        else:
            return True

    def log_results(self):
        """
        Report formatting in order to show results at user
        """
        self._logger.info(str(self.server.ssh_config.results.count(0)) + " warnings in SSH configuration")

    def print_results(self):
        """
        Print results of the analysis
        """
        print "=============================================================================="
        print "==                       Cron analysis results                              =="
        print "=============================================================================="
        print ("Warning, this analysis is very limited. The cron daemon is a complex tool. It requires Crontab and Anacron. "
               "See the man for more precision on this fields.\n"
               "This scenario check the content of /var/spool/cron/crontabs\n"
               "It checks if the first path found in a line is referenced in the imported file list. Then, it checks the rights to prevent a writtable "
               "file by non-proprietary user.\n\n")
        print "Content of the /var/spool/cron/crontabs file : \n"
        for user, command in self.server.crontab_config.items():
            print "USER : " + str(user)
            print command
        print"\nFiles checked :\n"
        for file_checked in self.server.crontab_results:
            print file_checked

if __name__ == "__main__":
    import doctest
    doctest.testmod()

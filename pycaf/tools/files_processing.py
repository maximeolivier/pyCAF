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
Created on Tue Apr  8 09:49:19 2014

@author: thierry
"""

import urllib2
import os
import hashlib
import gzip
from pycaf.tools.logs import create_logger


def checkInternetAccess(config):
    """
    Function which instanciate an internet connection and return True if it is established
    """
    logger = create_logger(__name__, config)

    try:
        adress = "https://www.google.com"
        urllib2.urlopen(adress)
        logger.debug("Internet access available")
        return True
    except urllib2.URLError, e:
        logger.warning("Internet connection unavailable")
        logger.warning(e)
        return False


def downloadFile(url, name, config, path=None):
    """
    Download a file according to the url and saved it at the path+name
    """
    logger = create_logger(__name__, config)

    if path is None:
        pathTest = "/tmp/"
    else:
        pathTest = path

    if not os.path.exists(path):
        os.makedirs(path)

    pathTest += name

    logger.debug("URL : "+str(url))
    logger.debug("Download path : "+str(pathTest))

    try:
        u = urllib2.urlopen(url)
        file_md5 = make_url_md5(url)

    except urllib2.HTTPError, e:
        logger.error("HTTP error : "+str(e.code))
        return False

    except urllib2.URLError, e:
        logger.error("URL error : "+str(e.reason))
        logger.error("Cannot access to : "+url)
        return False

    except Exception:
        import traceback
        logger.error("Generic exception : " + traceback.format_exc())
        return False

    md5saved = None
    # Check if a file ever exist
    if os.path.exists(pathTest):
        # if the file is up to date through md5
        f = gzip.open(pathTest, 'rb')
        lines = f.readlines()
        f.close()
        md5saved = lines[len(lines)-1]
        logger.debug("md5 saved = "+str(md5saved))

    if md5saved is not None and md5saved == file_md5:
        logger.debug("Stored file "+str(name)+" ever up to date")
        return True
    else:

        meta = u.info()

        f = open(pathTest, 'wb')
        file_size = int(meta.getheaders("Content-Length")[0])

        logger.debug("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        count_bp = 1

        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            p = float(file_size_dl) / file_size

            # Print bar progress every 10 % progress
            if p > (0.1 * count_bp):
                count_bp += 1
                status = "{0}  [{1:.2%}]".format(file_size_dl, p)
                logger.debug(status)
            # sys.stdout.flush()

        status = "{0}  [{1:.2%}]".format(file_size_dl, p)
        logger.debug(status)
        logger.debug("Download finished file :\n" + pathTest)
        f.close()

        f = gzip.open(pathTest, 'ab')
        f.write("\n\n")
        f.write(file_md5)
        f.close()

        return True


def make_url_md5(url):
    """
    Create a md5 hash with an url header. The hash is processed with the last-modified date,
    the expiration date and the content-length.
    """
    u = urllib2.urlopen(url)
    infoHeader = str(u.info().getheaders("Last-Modified"))
    infoHeader += str(u.info().getheaders("Expires"))
    infoHeader += str(u.info().getheaders("Content-length"))

    u1 = hashlib.md5(infoHeader).hexdigest()
    return u1


def save_pickle(object_to_save, path_to_save):
    """
    Function which save an object with the pickle library
    """
    import pickle

    try:
        archive = open(path_to_save, 'wb')
        pickle.dump(object_to_save, archive)
        archive.close()
    except IOError:
        print "Failed pickle saving : remember to put the entire filename : path/filename."


def load_pickle(filename):
    """
    Function which load an object saved with the pickle library
    """
    import pickle

    try:
        pkl_file = open(filename, 'rb')
        data = pickle.load(pkl_file)
        return data
    except IOError:
        print "Failed pickle loading : remember to put the entire filename path."


def compare_rights(rights1, rights2):
    """
    Compare two rights string of 10 characters.
    It is possible to replace r,w or x by '*'.
    For example :
    rights1 = "-rwxr-xr-x"
    rights2 = "-r**r**r-x"
    This rights will matched True !
    """
    match_flag = False
    mismatch_count = 0
    if len(rights1) != 10 and len(rights2) != 10:
        print "Bad rights arguments"
        return False
    else:
        for j, c_right in enumerate(rights2):
            if rights1[j] != c_right and c_right != '*':
                mismatch_count += 1
        if mismatch_count == 0:
            match_flag = True
    return match_flag


def filter_objects(object_list_in, *args, **kwargs):
    """
    Function wich filter a classic list of object [] with params args and kwargs
    The param args contains integer and the function return a list of object corresponding to this indexes
    The param kwargs contains attributes and values like this : attribut1="value1, value2", attribut2="val",...
    The filtering works with a white list and a black list. If any attribute's value is blacklisted, the object is filtered.
    All conditions of the white list have to be right in order to pass the filtering.
    """
    object_list_out = []

    if len(object_list_in) == 0:
        print "Object list empty"
        return False

    if len(kwargs) == 0 and len(args) == 0:
        return object_list_in

    if len(args) != 0:
        for nb_id in args:
            object_list_out.append(object_list_in[nb_id - 1])

    if len(kwargs) != 0:
        # We make an empty white list and a black list of attributes
        white_attr = []
        black_attr = []

        # We create the list of possible filtering attributes
        args_availables = object_list_in[0].__dict__.keys()
        hide_list = []
        for arg_available in args_availables:
            hide_list.append("hide_" + str(arg_available))
        args_availables += hide_list

        # We check that the attributes are coorect and we put in the white and black lists
        for arg in kwargs:
            if arg not in args_availables:
                print "Argument incorrect, check your input"
                return False
            elif "hide_" in arg:
                black_attr.append(arg)
            else:
                white_attr.append(arg)

        # We make an empty white and black dictionnary to contain attribut and value(s)
        white_dict = {}
        black_dict = {}

        # We fill black and white dictionnary of attributes and values
        # Need to add a number to differenciate attributes in the dictionnary
        for key in kwargs:
            list_values = kwargs[key].split(',')
            # Remove spaces in values and put in the black and white list
            for i, val in enumerate(list_values):
                k = str(key) + "__" + str(i)
                if "hide_" in key:
                    black_dict[k] = val.strip()
                else:
                    white_dict[k] = val.strip()

        for obj in object_list_in:
            show_black = True
            if len(black_dict) > 0:
                for attr in black_dict:
                    obj_attr = (attr.split("__")[0]).split("hide_")[1]
                    if black_dict[attr] == getattr(obj, obj_attr):
                        show_black = False
                        break
            # If the object is black listed, we stop the filtering and we process the next object
            if show_black:
                show_white = True
                if len(white_dict) > 0:
                    for attr in white_dict:
                        obj_attr = attr.split("__")[0]
                        if white_dict[attr] != getattr(obj, obj_attr):
                            show_white = False
                            break

                    if show_white:
                        object_list_out.append(obj)
                else:
                    object_list_out.append(obj)

    return object_list_out

#!/usr/bin/env python

import logging
import yaml
import os

LOGGER_NAME = 'atto'
logger = logging.getLogger()

def init_logging(log_name="server.log", log_path='../logs/', log_foramt="", log_level=3):
    logger = logging.getLogger()
    hdlr = logging.FileHandler(os.path.join(log_path, log_name))
    formatter = logging.Formatter(log_foramt)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(log_level * 3)


def check_file(file_path):
    if not os.path.exists(file_path):
        raise IOError("File not found: %s", file_path)
    elif not os.path.isfile(file_path):
        raise IOError("Path is not a file: %s", file_path)
    return True

def check_dir(dir_path):
    if not os.path.exists(dir_path):
        raise IOError("Directory not found: %s", dir_path)
    elif not os.path.isdir(dir_path):
        raise IOError("Path is not a directory: %s", dir_path)
    return True

def load_yaml_file(file_path):
    if check_file(file_path):
        with open(file_path, 'r') as f:
            try:
                return yaml.load(f.read())
            except yaml.YAMLError as e:
                logger.error("Trouble reading yaml file: %s", file_path)
                raise e
    return {}

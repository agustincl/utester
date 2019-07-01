#!/usr/bin/env python
# # -*- coding: utf-8 -*-

# TODO: Modify the help message based on all the hardware checks
"""
Unit test the hardware of a machine.
 - Test Producer from command lines. This will autocreate a topic named 'utester'
 - Test Delete topic
 - Test Describe resource with filter

To test consumer is working, on kafka server try:
    kafka-console-consumer --bootstrap-server localhost:9092 --topic utester --from-beginning

Example:
    Create lines
        python utKafka.py -b 192.168.56.51:9092 -pl

    Describe topic
        python utKafka.py -b 192.168.56.51:9092 -d topic -cf utester

    Delete Topic
        python utKafka.py -b 192.168.56.51:9092 -dt

"""

import argparse
import logging
import json
import socket

from pathlib import Path
from argparse import RawTextHelpFormatter
from typing import List, Dict

from helpers.utils import *
#from helpers.hardware import *

log = logging.getLogger(Path(__file__).stem)
logfile = 'operations.log'
version = "1.0"


def check_hardware(config: Dict):
    log.debug("------------------ Begin check_hardware ------------------")
    log_trace = 'None'
    status = 'Ok'

    # Obtain the configuration for the machine type specified in the CLI arguments
    machine_type = config['type']
    machine_uthardware_config = next(filter(lambda machine_conf: machine_conf['type'] == machine_type, config['uthardwareconfig']))
    assert type(machine_uthardware_config) == dict
    assert machine_uthardware_config['type'] == machine_type

    # Obtain the fully qualified domain name
    fqdn = socket.getfqdn()

    # ------------------------- Switch options ------------------------- #
    if machine_type == 'bastion':
        check_bastion(machine_uthardware_config)

    if machine_type == 'kafka':
        check_kafka(machine_uthardware_config, fqdn)

    if machine_type == 'striim':
        check_striim(machine_uthardware_config, fqdn)

    if machine_type == 'psql':
        check_psql(machine_uthardware_config, fqdn)

    if machine_type == 'emr':
        check_emr(machine_uthardware_config, fqdn)

    if machine_type == 'redis':
        check_redis(machine_uthardware_config)

    # TODO: In the image there is another psql
    # ------------------------------------------------------------------ #
    
    log_trace = "Send " + status + " | " + log_trace
    log.debug("------------------ End check_hardware ------------------")
    return {"logtrace": log_trace, "status": status}


# ---------------- BEGIN Machine checks ---------------- #

def check_bastion(bastion_config):
    # TODO
    pass


def check_kafka(kafka_config, fqdn):
    check_fs(kafka_config['hardware']['fs'])


def check_striim(striim_config, fqdn):
    # TODO
    pass


def check_psql(psql_config, fqdn):
    # TODO
    pass


def check_emr(emr_config, fqdn):
    # TODO
    pass


def check_redis(redis_config):
    # TODO
    pass


# ---------------- END Machine checks ---------------- #

# ---------------- BEGIN Unit checks ---------------- #


def check_fs(mountpoints: List[str]):
    # TODO
    pass


# ---------------- END Unit checks ---------------- #

def main(args, loglevel):
    if args.logging:
        logging.basicConfig(filename=logfile, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=loglevel)
    logging.info('Started check_hardware')
    log.debug("------------------ Reading config ------------------")

    # Parse the configfile
    configfile_json = json.load(open(os.path.realpath(args.configfile)))
    # Obtain the JSON object with the utHardware configuration
    uthardwareconfig = configfile_json['utHardware']

    config = {
        'uthardwareconfig': uthardwareconfig,
        'type': args.type,
    }
    config['root_dir'] = os.path.dirname(os.path.abspath(__file__))

    hw_info = check_hardware(config)

    print("Done.")
    logging.info('Finished check_hardware')
    exit_to_icinga(hw_info)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + version)

    # TODO: default="none" or default=None or without default?
    parser.add_argument('-c', '--configfile', help='Configuration file path (.json).', type=str, default=None, required=True)
    parser.add_argument('-t', '--type', help='Machine type (i.e. kafka).', type=str, default=None, required=True)

    parser.add_argument('-l', '--logging', help='create log output in current directory', action='store_const', const=True, default=False)
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', help='increase output verbosity', action='store_const', const=logging.DEBUG, default=logging.INFO)
    verbosity.add_argument('-q', '--quiet', help='hide any debug exit', dest='verbose', action='store_const', const=logging.WARNING)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args, args.verbose)

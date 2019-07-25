#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
Send metrics from Python to a file with the Prometheus format.
Metric types:
 - Counter.
 - Gauge.
 - Histogram.
 - Summary.

Example:
    TODO

"""

import argparse
import logging
import time
from argparse import RawTextHelpFormatter

from prometheus_client import CollectorRegistry, Gauge, write_to_textfile, Counter, Histogram

from helpers.utils import *

log = logging.getLogger(os.path.splitext(__file__)[0])
logfile = 'operations.log'
version = "1.0"


def emit_metric(config):
    log.debug("------------------ Begin emit_metric ------------------")
    log_trace = 'None'
    status = 'Ok'

    # Create registry to collect the metric. A separate registry is used,
    # as the default registry may contain other metrics such as those from the Process Collector.
    registry = CollectorRegistry()

    # ------------------------- Switch options ------------------------- #
    # At least one option must be passed
    if not (config['counter'] or config['gauge'] or config['histogram'] or config['summary']):
        error_message("At least one of this options must be passed: -c/--counter, -g/--gauge, -hi/--histogram, -s/--summary\n")

    # In this case, all options can be used at the same time
    if config['counter']:
        emit_counter_metric(registry, config['metricname'], config['metricdescription'], config['counter'])
    if config['gauge']:
        emit_gauge_metric(registry, config['metricname'], config['metricdescription'], config['gauge'])
    if config['histogram']:
        emit_histogram_metric(registry, config['metricname'], config['metricdescription'], config['histogram'])
    if config['summary']:
        emit_summary_metric(registry, config['metricname'], config['metricdescription'], config['summary'])
    # ------------------------------------------------------------------ #

    # Send the metrics to the specified file
    file_path: str = config['file']
    write_to_textfile(file_path, registry)

    log_trace = "Send " + status + " | " + log_trace
    log.debug("------------------ End emit_metric ------------------")
    return {"logtrace": log_trace, "status": status}


def emit_counter_metric(registry: CollectorRegistry, metric_name: str, metric_description: str, increment_value: float):
    """
    Emits a metric of type Counter, incrementing it's initial value (0.0) with the given value.
    """
    try:
        counter = Counter(metric_name, metric_description, registry=registry)
        counter.inc(increment_value)
        ok_message("Metric '{}' incremented in value '{}'".format(metric_name, increment_value))
    except Exception as error:
        error_message("Error while emitting Counter metric: {}".format(error))


def emit_gauge_metric(registry: CollectorRegistry, metric_name: str, metric_description: str, value: float):
    """
    Emits a metric of type Gauge, with the given value.
    """
    try:
        gauge = Gauge(metric_name, metric_description, registry=registry)
        gauge.set(value)
        ok_message("Metric '{}' value setted to '{}'".format(metric_name, value))
    except Exception as error:
        error_message("Error while emitting Gauge metric: {}".format(error))


# TODO
def emit_histogram_metric(registry: CollectorRegistry, metric_name: str, metric_description: str, seconds: float):
    """
    Emits a metric of type Histogram.
    """
    try:
        pass
    except Exception as error:
        error_message("Error while emitting Histogram metric: {}".format(error))


# TODO
def emit_summary_metric(registry: CollectorRegistry, metric_name: str, metric_description: str, value: float):
    """
    Emits a metric of type Summary.
    """
    try:
        pass
    except Exception as error:
        error_message("Error while emitting Summary metric: {}".format(error))


def main(args, loglevel):
    if args.logging:
        logging.basicConfig(filename=logfile, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=loglevel)
    logging.info('Started emit_metric')
    log.debug("------------------ Reading config ------------------")

    config = {
        'file': args.file,
        'metricname': args.metricname,
        'metricdescription': args.metricdescription,
        'counter': args.counter,
        'gauge': args.gauge,
        'histogram': args.histogram,
        'summary': args.summary,
    }
    config['root_dir'] = os.path.dirname(os.path.abspath(__file__))

    _info = emit_metric(config)

    print("Done.")
    logging.info('Finished emit_metric')
    exit_to_icinga(_info)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + version)

    parser.add_argument('-f', '--file', help='Path to the file where the metrics will be saved', type=str, default=None, required=True)
    parser.add_argument('-mn', '--metricname', help='Metric name', type=str, default=None, required=True)
    parser.add_argument('-md', '--metricdescription', help='Metric description', type=str, default=None, required=True)

    parser.add_argument('-c', '--counter', help='Emit a metric of type Counter. The value of this param is the value used to increment the counter.',
                        type=float, default=None)
    parser.add_argument('-g', '--gauge', help='Emit a metric of type Gauge. The value of this param is the value of the gauge metric.',
                        type=float, default=None)
    parser.add_argument('-hi', '--histogram', help='Emit a metric of type Histogram', action='store_const', const=True, default=False)
    parser.add_argument('-s', '--summary', help='Emit a metric of type Summary', action='store_const', const=True, default=False)

    parser.add_argument('-l', '--logging', help='create log output in current directory', action='store_const', const=True, default=False)
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', help='increase output verbosity', action='store_const', const=logging.DEBUG, default=logging.INFO)
    verbosity.add_argument('-q', '--quiet', help='hide any debug exit', dest='verbose', action='store_const', const=logging.WARNING)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args, args.verbose)

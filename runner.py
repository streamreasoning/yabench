#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import subprocess
import os
import errno
from string import Template

INPUTSTREAM_PREFIX = 'SG_'
QUERYRESULTS_PREFIX = 'QR_'
QUERY_PREFIX = "QUERY_"
ORACLE_OUTPUT_PREFIX = "ORACLE_"

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def gen_test_config(config, test_config):
    new_dict = config.copy()
    del new_dict['tests']
    new_dict.update(test_config)
    return new_dict

def prepare_query(resultsDir, config, queryFile):
    try:
        with open(queryFile) as f:
            t = Template(f.read())

        qF = "{}/{}{}".format(resultsDir, QUERY_PREFIX, config['name'])
        with open(qF, 'w') as q:
            query = t.substitute(config['vars'])
            q.write(query)
        return qF
    except IOError:
        print('Can\'t open {} file!'.format(queryFile))

def runGenerator(resultsDir, config):
    run_args = ["java", "-jar", config['exec']['stream-generator']]
    run_args.extend(["-dest", "{}/{}{}".format(resultsDir, INPUTSTREAM_PREFIX, config['name'])]);
    run_args.extend(["-name", config['generator']]);
    run_args.extend(["-duration", config['duration']]);
    run_args.extend(["-seed", config['seed']]);
    run_args.extend(["-stations", config['stations']]);
    run_args.extend(["-interval", config['interval']]);
    if 'max_temp' in config:
        run_args.extend(["-max_temp", config['max_temp']]);
    if 'min_temp' in config:
        run_args.extend(["-min_temp", config['min_temp']]);

    print(run_args)
    return subprocess.check_call(run_args)

def runEngine(testDir, resultsDir, config):
    run_args = ["java", "-jar", config['exec']['engine']]
    run_args.extend(["-dest", "{}/{}{}".format(resultsDir, QUERYRESULTS_PREFIX, config['name'])])
    run_args.extend(["-query", prepare_query(resultsDir, config, "{}/{}".format(testDir, config['query']))])
    run_args.extend(["-source", "{}/{}{}".format(resultsDir, INPUTSTREAM_PREFIX, config['name'])])

    print(run_args)
    return subprocess.check_call(run_args)

def runOracle(resultsDir, config):
    run_args = ["java", "-jar", config['exec']['oracle']]
    run_args.extend(["-queryresults", "{}/{}{}".format(resultsDir, QUERYRESULTS_PREFIX, config['name'])])
    run_args.extend(["-output", "{}/{}{}".format(resultsDir, ORACLE_OUTPUT_PREFIX, config['name'])])
    run_args.extend(["-inputstream", "{}/{}{}".format(resultsDir, INPUTSTREAM_PREFIX, config['name'])])
    run_args.extend(["-test", config['oracle_test']])
    run_args.extend(["-windowsize", config['window']['size']])
    run_args.extend(["-windowslide", config['window']['slide']])

    #Test specific arguments
    run_args.extend(["-temp", config['temp']])

    print(run_args)
    return subprocess.check_call(run_args)

def main():
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument('testDir')

    args = parser.parse_args()

    resultsDir = args.testDir + '/results'
    make_sure_path_exists(resultsDir)

    try:
        with open(args.testDir + '/config.json') as configFile:
            config = json.load(configFile)
            for test_config in config['tests']:
                new_config = gen_test_config(config, test_config)
                runGenerator(resultsDir, new_config)
                runEngine(args.testDir, resultsDir, new_config)
                runOracle(resultsDir, new_config)
    except IOError:
        print("Can\'t open {}/config.json file".format(args.testDir))

if __name__ == '__main__':
    main()
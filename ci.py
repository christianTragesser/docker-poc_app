#!/usr/bin/python3
import os
from argparse import ArgumentParser
from poc import POC

dirPath = os.path.dirname(os.path.realpath(__file__))
pipeline = POC(dockerRegistry='registry.gitlab.com/')
localTag = 'local/poc_app'

def ci(option):
    stage = {
        'test': test,
        'scan': securityScan,
        'local': local,
        'qa': qa
    }
    run = stage.get(option, None)
    if run:
        run()
    else:
        print("'{}' not a valid option".format(option))
        exit(1)

def test():
    print('Starting tests:')
    pipeline.unit_test(dirPath)
    pipeline.build_image(dirPath,localTag)
    pipeline.uat_test(dirPath)
    print('Testing complete')

def securityScan():
    print('Starting security scans:')
    pipeline.cve_scan(localTag)

def local():
    print('Initializing locally built instance:')
    pipeline.build_image(dirPath,localTag)
    pipeline.run_local()

def qa():
    print('Starting POC app:')
    pipeline.run_latest()

def main():
    parser = ArgumentParser(prog='ci-py')
    parser.add_argument('option', type=str,
                        help='run pipeline option; test, scan, local, qa')
    args = parser.parse_args()
    ci(args.option)

if __name__ == '__main__':
    main()

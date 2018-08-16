#!/usr/bin/python
import os
from argparse import ArgumentParser
from poc import POC

dirPath = os.path.dirname(os.path.realpath(__file__))

pipeline = POC(dockerRegistry='christiantragesser')

def ci(option):
    stage = {
        'test': test,
        'scan': securityScan,
        'local': local,
        'qa': qa
    }
    run = stage.get(option, test)
    run()

def test():
    print('Starting tests:')
    pipeline.buildImage(dirPath,'local/poc_app')
    pipeline.uatTest(dirPath)
    print('Testing complete')

def securityScan():
    print('Starting security scans:')
    pipeline.cveScan('local/poc_app')

def local():
    print('Initializing locally built instance:')
    pipeline.buildImage(dirPath,'local/poc_app')
    pipeline.runLocal()

def qa():
    print('Starting POC app:')
    pipeline.runLatest()

def main():
    parser = ArgumentParser(prog='dind-ci-py')
    parser.add_argument('option', type=str,
                        help='run pipeline option; test, scan, local, qa')
    args = parser.parse_args()
    ci(args.option)

if __name__ == '__main__':
    main()
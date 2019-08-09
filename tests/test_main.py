import pytest
import mock
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main

'''
  # gets hostname, IP address, and git sha version and returns
'''
@mock.patch('socket.gethostbyname', return_value='1.1.1.1')
@mock.patch('socket.gethostname', return_value='testhost')
def test_get_host_data(mock_socket_gethostname, mock_socket_gethostbyname):
    hostData = main.get_host_data()
    assert hostData['name'] == 'testhost'
    assert hostData['ip'] == '1.1.1.1'
    assert hostData['sha'] == 'non-pipeline build'


'''
  # takes in host data, pretty print data
'''
hostInfoResponse = { 'name': 'testhost', 'ip': '1.1.1.1', 'sha': 'testbuild'}
@mock.patch('main.pretty_print')
@mock.patch('main.get_host_data', return_value=hostInfoResponse)
def test_route_root(mock_get_hostdata, mock_prettyPrint):
    main.route_root()
    mock_prettyPrint.assert_called()

'''
  # get hostname data, returns git sha json
'''
@mock.patch('main.get_host_data', return_value=hostInfoResponse)
def test_route_status(mock_get_hostdata):
    status = json.loads(main.route_status())
    assert status == {'sha': 'testbuild'}
#!/bin/bash

test -f /var/www/html/index.php
fileResult=$?

if [ $fileResult -eq 0 ]; then
  echo "+ index.php file exists"
else
  echo "- index.php file not found" && exit $fileResult
fi

netstat -pultn | grep --quiet 80
netstatResult=$?

if [ $netstatResult -eq 0 ]; then
  echo "+ httpd service listening on tcp port"
else
  echo "- http service not listening on tcp port" && exit $netstatResult
fi

curl -s 127.0.0.1 | grep --quiet "Server hostname"
curlResult=$?

if [ $curlResult -eq 0 ]; then
  echo "+ website content seen"
else
  echo "- website content not seen" && exit $curlResult
fi

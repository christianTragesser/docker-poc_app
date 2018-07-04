#!/bin/bash

echo -e "\n****** starting automated tests ********\n"

curl -s $1 | grep --quiet "Server hostname"
hostResult=$?

if [ $hostResult -eq 0 ]; then
  echo "+ hostname content seen"
else
  echo "- hostname content not seen" && exit $hostResult
fi

curl -s $1 | grep --quiet "Server LAN IP address"
ipResult=$?

if [ $ipResult -eq 0 ]; then
  echo "+ LAN IP content seen"
else
  echo "- LAN IP content not seen" && exit $ipResult
fi

curl -s $1 | grep --quiet "background-color:white"
backgroundResult=$?

if [ $backgroundResult -eq 0 ]; then
  echo "+ background color check passed"
else
  echo "- background color check failed" && exit $backgroundResult
fi

echo -e "\n****** testing complete ********\n"
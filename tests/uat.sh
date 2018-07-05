#!/bin/bash

echo -e "\nImplementing tests:"

curl -s $1 | grep --quiet "Server hostname"
hostResult=$?

if [ $hostResult -eq 0 ]; then
  echo -e "\t+ hostname content seen"
else
  echo -e "\t- hostname content not seen" && exit $hostResult
fi

curl -s $1 | grep --quiet "Server LAN IP address"
ipResult=$?

if [ $ipResult -eq 0 ]; then
  echo -e "\t+ LAN IP content seen"
else
  echo -e "\t- LAN IP content not seen" && exit $ipResult
fi

curl -s $1 | grep --quiet "background-color:white"
backgroundResult=$?

if [ $backgroundResult -eq 0 ]; then
  echo -e "\t+ background color check passed"
else
  echo -e "\t- background color check failed" && exit $backgroundResult
fi
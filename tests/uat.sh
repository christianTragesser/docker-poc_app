#!/bin/bash

CHECKMARK="\xE2\x9C\x94"
CROSSBONES="\xE2\x98\xA0"
echo -e "\n UAT testing:"

curl -s $1 | grep --quiet "Hostname:"
hostResult=$?

if [ $hostResult -eq 0 ]; then
  echo -e "\t$CHECKMARK  Hostname content seen"
else
  echo -e "\t$CROSSBONES  Hostname content not seen" && exit $hostResult
fi

curl -s $1 | grep --quiet "Local IP:"
ipResult=$?

if [ $ipResult -eq 0 ]; then
  echo -e "\t$CHECKMARK  LAN IP content seen"
else
  echo -e "\t$CROSSBONES  LAN IP content not seen" && exit $ipResult
fi

curl -s $1 | grep --quiet "background-color:white"
backgroundResult=$?

if [ $backgroundResult -eq 0 ]; then
  echo -e "\t$CHECKMARK  Background color check passed"
else
  echo -e "\t$CROSSBONES  Background color check failed" && exit $backgroundResult
fi

curl -s "${1}/status" | grep --quiet "sha"
statusResult=$?

if [ $statusResult -eq 0 ]; then
  echo -e "\t$CHECKMARK  Status endpoint passed"
else
  echo -e "\t$CROSSBONES  Status endpoint failed" && exit $statusResult
fi
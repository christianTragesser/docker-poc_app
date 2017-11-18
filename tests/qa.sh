curl -s 127.0.0.1 | grep --quiet "background-color:white"
curlResult=$?

if [ $curlResult -eq 0 ]; then
  echo "+ background color check passed"
else
  echo "- background color check failed" && exit $curlResult
fi

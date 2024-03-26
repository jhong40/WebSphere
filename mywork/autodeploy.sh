#!/bin/bash
while true
do
  if [ deployrequest.txt -nt deployed.txt ]; then
    touch deployed.txt
    pgrep dd.sh | wc -l > a.txt
    line=$(head -n 1 a.txt)
    #echo $line
    if [[ "line" -eq "1" ]]; then
      echo "starting deployment...."
      sleep  10
      echo "deployment end....."
    else
      echo "Another deployment is running. Wait until it finishes, it will start a new one"    fi
  fi
  echo "while sleep..."
  sleep 10
done

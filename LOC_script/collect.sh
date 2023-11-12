#! /bin/bash
rm result
while IFS="," read -r url commit
do
  echo -n "url:$url " >> result
  echo -n "commit: $commit " >> result
  echo -n "loc: " >> result
  echo "cloning repo"
  git clone $url temp
  cd temp
  cloc $commit timeout 0 --json | jq .SUM.code | tee -a ../result
  cd ..
  rm -r temp
  echo "remove repo"
done < apps.csv

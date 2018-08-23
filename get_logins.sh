cat allresult.txt |  grep "2018/8" | sed 's/  .*//' | sed 's/.* //' | sort -u > aug2018.csv

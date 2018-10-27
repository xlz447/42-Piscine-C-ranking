cat result.txt |  grep "2018/10" | sed 's/  .*//' | sed 's/.* //' | sort -u > oct2018.csv

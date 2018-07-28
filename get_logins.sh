cat final_results.txt |  grep "2018/5" | sed 's/  .*//' | sed 's/.* //' | sort -u > may2018.csv

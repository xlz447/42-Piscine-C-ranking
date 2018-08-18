cat final_results.txt |  grep "2017/10" | sed 's/  .*//' | sed 's/.* //' | sort -u > oct2017.csv


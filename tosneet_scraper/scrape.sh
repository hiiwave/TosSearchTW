for spiderid in npcs skills attributes zones items
do
  echo "===================="
  echo "Scraping $spiderid.."
  echo "===================="
  fname="output/$spiderid.json"
  rm -f $fname
  scrapy crawl $spiderid -o $fname
done


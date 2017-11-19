sudo su ec2-user
python3 /home/icorium/cron/reset-tables.py

cd /home/icorium/icoriumcrawl/Crawler
/usr/local/bin/scrapy crawl tokenmarket -L WARNING -o /home/icorium/csv/tokenmarket.csv > /home/icorium/log/tokenmarket.log
/usr/local/bin/scrapy crawl icorating -L WARNING -o /home/icorium/csv/icorating.csv > /home/icorium/log/icorating.log
/usr/local/bin/scrapy crawl icolist -L WARNING -o /home/icorium/csv/icolist.csv > /home/icorium/log/icolist.log
/usr/local/bin/scrapy crawl smithandcrown -L WARNING -o /home/icorium/csv/smithandcrown.csv > /home/icorium/log/smithandcrown.log
/usr/local/bin/scrapy crawl coinschedule -L WARNING -o /home/icorium/csv/coinschedule.csv > /home/icorium/log/coinschedule.log

python3 /home/icorium/cron/match-ico.py
python3 /home/icorium/cron/create-csv.py

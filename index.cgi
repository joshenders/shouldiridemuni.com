#!/bin/bash

# http header
printf "Content-Type: text/html; charset=utf-8\n\n"

# html head
printf '<!doctype html><html><!-- http://github.com/joshenders/ --><head><meta charset="utf-8" /><title>Should I ride Muni today?</title><style type="text/css">p { font-family: Helvetica, Arial, sans-serif; font-weight: bold; } .big { font-size: 120pt; color: black; margin: 0px; } .time { font-size: 25pt; color: #595959; } .small { font-size: 25pt; color: gray; } .query { font-size: 45pt; color: gray; }</style></head><body style="text-align: center">'

# A cron job grabs the schedule twice a day at noon and midnight
# 00 00,12 * * * /usr/bin/curl -s "http://mlb.mlb.com/soa/ical/schedule.csv?home_team_id=137&season=$(date +%Y)" | /bin/egrep 'START|AT&T' | /usr/bin/cut -d, -f1,2,9 > schedule.csv

schedule='schedule.csv'
today="$(date +%m/%d/%y)" # mm/dd/yy is the format of schedule.csv
#now=$(date "+%I:%M %p")

# input is comma seperated
IFS=,

# loop through schedule
while read field1 field2 field3; do
  if [[ "$field1" =~ "$today" ]]; then
    game='1'
    begins="$field2"
    ends="$field3"
    break
  fi
done < "$schedule"

# html main
printf "<p class=\"query\">Should I ride Muni today?</p>"

if [[ -n "$game" ]]; then # there's a game today
    printf "<p class=\"big\">Nope.</p><p class=\"small\">The Giants are playing a home game that starts at <span class=\"time\">$begins</span> and ends at <span class=\"time\">$ends</span>.</p>"
else
    printf "<p class=\"big\">Sure.</p><p class=\"small\">No Giants game today.</p>"
fi

# html tail
printf "<script type=\"text/javascript\">var _gaq = _gaq || []; _gaq.push(['_setAccount', 'UA-12542183-3']); _gaq.push(['_trackPageview']); (function() { var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true; ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js'; var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s); })();</script></body></html>"

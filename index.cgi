#!/bin/bash

# http header
printf "Content-Type: text/html; charset=utf-8\n\n"

# html head
printf '<!doctype html><html><!-- http://josh.typepad.com --><head><meta charset="utf-8" /><title>Should I ride Muni today?</title><style type="text/css">p { font-family: Helvetica, Arial, sans-serif; font-weight: bold; } .big { font-size: 120pt; color: black;} .small { font-size: 25pt; color: gray; }</style></head><body style="text-align: center; padding-top: 100px;">'

# It's rather sloppy, but a cron does this:
# @daily curl -s "http://mlb.mlb.com/soa/ical/schedule.csv?home_team_id=137&season=$(date +%Y)" | egrep 'START|AT&T' | cut -d, -f1,2,9 > schedule.csv

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
printf "<p class=\"small\">Should I ride Muni today?</p>"

if [[ -n "$game" ]]; then # there's a game today
    printf "<p class=\"big\">No.</p><p class=\"small\">The Giants are playing a home game that starts at $begins and ends at $ends</p>"
else
    printf "<p class=\"big\">Yes.</p><p class=\"small\">The Giants aren't playing a home game</p>"
fi

# html tail
printf "<script type=\"text/javascript\">var _gaq = _gaq || []; _gaq.push(['_setAccount', 'UA-12542183-3']); _gaq.push(['_trackPageview']); (function() { var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true; ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js'; var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s); })();</script></body></html>"

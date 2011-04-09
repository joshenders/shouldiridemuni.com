#!/bin/bash

# http://mlb.mlb.com/soa/ical/schedule.csv?home_team_id=137&season=2011

echo -en "Content-Type: text/html; charset=utf-8\n\n"

cat << EOF
<!doctype html>
<html>
  <!-- http://josh.typepad.com -->
  <head>
    <meta charset="utf-8" />
    <title>Should I ride Muni?</title>
  </head>
  <body style="text-align: center; padding-top: 200px;">
EOF

schedule=schedule.csv
today=$(date +%m/%d/%y) # mm/dd/yy is the format of schedule.csv
#now=$(date "+%I:%M %p")

IFS=,

line=0
while read field1 field2 field3; do
  if [[ "$field1" =~ "$today" ]]; then
    game=1
    begins=$field2
    ends=$field3
    break
  fi
done < $schedule

if [[ -n "$game" ]]; then
    echo -e "    <p style=\"font-size: 120pt; font-weight: bold; font-family: Helvetica, Arial, sans-serif; color: black;\">No.</p>"
else
    echo -e "    <p style=\"font-size: 120pt; font-weight: bold; font-family: Helvetica, Arial, sans-serif; color: black;\">Yes.</p>"
fi

cat << EOF
    <script type="text/javascript">var _gaq = _gaq || []; _gaq.push(['_setAccount', 'UA-12542183-3']); _gaq.push(['_trackPageview']); (function() { var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true; ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js'; var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s); })();</script>
  </body>
</html>
EOF

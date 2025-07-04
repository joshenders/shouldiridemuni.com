#!/usr/bin/env bash

# http header
printf "Content-Type: text/html; charset=utf-8\n\n"

# html head
printf '<!doctype html><html><!-- https://github.com/joshenders/shouldiridemuni.com --><head><meta charset="utf-8" /><link rel="canonical" href="https://shouldiridemuni.com" /><link rel="icon" type="image/png" href="data:image/png;base64,AAABAAEAEBACAAAAAACwAAAAFgAAACgAAAAQAAAAIAAAAAEAAQAAAAAAQAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAQACwAKPFAACn5QAAp+UAAK51AACsNQAAqZUAAKvVAACr1QAAq9UAAKvVAACr1QAAu90AAJPJAADGYwAA/n8AAHw+AABcOgAAWBoAAFgaAABRigAAU8oAAFZqAABUKgAAVCoAAFQqAABUKgAAVCoAAEQiAABsNgAAOZwAAAGAAACDwQAA" /><title>Should I ride Muni today?</title><style type="text/css">* { font-family: Helvetica, Arial, sans-serif; font-weight: bold; } .big { font-size: 120pt; color: black; margin: 0px; } .time { font-size: 30pt; color: #595959; } h1 { font-size: 45pt; color: gray; } .small { font-size: 25pt; color: gray; }</style><script async src="https://www.googletagmanager.com/gtag/js?id=G-MR7ZQL32ER"></script><script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);}; gtag('js', new Date());gtag('config', 'G-MR7ZQL32ER');</script></head><body style="text-align: center">'

# A cron job downloads the schedule at noon and midnight
# 00 00,12 * * * /usr/local/sbin/get-mlb-schedule.sh

# Sample lines:
# START DATE,START TIME,START TIME ET,SUBJECT,LOCATION,DESCRIPTION,END DATE,END DATE ET,END TIME,END TIME ET,REMINDER OFF,REMINDER ON,REMINDER DATE,REMINDER TIME,REMINDER TIME ET,SHOWTIMEAS FREE,SHOWTIMEAS BUSY
# 04/07/16,01:35 PM,04:35 PM,Dodgers at Giants,AT&T Park - San Francisco,"Local TV: CSN-BA ----- Local Radio: KNBR 680- KTRB 860",04/07/16,04/07/16,04:35 PM,07:35 PM,FALSE,TRUE,04/07/16,12:35 PM,03:35 PM,FREE,BUSY

# START DATE,START TIME,END TIME
schedule='schedule.csv'
today="$(date +%m/%d/%y)" # mm/dd/yy is the format of schedule.csv
#now=$(date "+%I:%M %p")

# input is comma seperated
IFS=,

# loop through schedule
while read field1 field2 field3; do
  if [[ "${field1}" == "${today}" ]]; then
    game='1'
    begins="${field2}"
    ends="${field3}"
    break
  fi
done < "${schedule}"

# html main
printf "<h1>Should I ride Muni today?</h1>"

if [[ -n "${game}" ]]; then # there's a game today
    printf "<p class=\"big\">Nope.</p><p class=\"small\">There's a Giants game today at Oracle Park.</p><p class=\"small\">It starts at <span class=\"time\">${begins}</span> and ends at <span class=\"time\">${ends}</span>.</p>"
else
    printf "<p class=\"big\">Sure.</p><p class=\"small\">No game today.</p>"
fi

# html tail
printf "</body></html>"

#!/bin/bash

year="$(date +%Y)"
outfile='/usr/share/nginx/shouldiridemuni.com/schedule.csv'
scheduleURL="https://www.ticketing-client.com/ticketing-client/csv/GameTicketPromotionPrice.tiksrv?team_id=137&home_team_id=137&display_in=singlegame&ticket_category=Tickets&site_section=Default&sub_category=Default&leave_empty_games=true&event_type=T&year=${year}&begin_date=${year}0101"

curl -s "${scheduleURL}" | cut -d, -f1,2,9 > "${outfile}"

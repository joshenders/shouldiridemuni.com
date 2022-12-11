# shouldridemuni.com

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## About

I built this site to be used while making split second transit decisions
during baseball season in San Francisco's SoMa district. After work you're
often faced with the question: "Should I take the bus or should I take the
Muni train home?"

In general, out-of-towners (Giants fans) don't understand the bus system and
use it far less than the train. The bus system is typically the slower option
but on game days, it's a lot faster and has seating room.

I can't overstate how bad the consequences are if you make the wrong choice...

## Performance

The page is optimized for extremely low cellular bandwidth. The whole page
fits in a very conservative TCP MSS of 1380 bytes. Sadly, I can't count on
0-RTT TLS, so no https (sorry).

## Improvements

It's currently written in Bash and runs as a CGI script. It should probably be
rewritten on Cloudflare's Workers platform.

## Installation

Runs via [https://acme.com/software/thttpd/](`thttpd`):

* `/etc/thttpd/thttpd.conf`
```
# BEWARE : No empty lines are allowed!
# This section overrides defaults
# This section _documents_ defaults in effect
# port=80
# nosymlink         # default = !chroot
# novhost
# nocgipat
# nothrottles
# host=0.0.0.0
# charset=iso-8859-1
host=127.0.0.1
port=10000
user=www-data
logfile=/var/log/thttpd.log
pidfile=/var/run/thttpd.pid
dir=/usr/share/nginx/shouldiridemuni.com
cgipat=**.sh|**.cgi
```

* `/etc/nginx/sites-available/shouldiridemuni.conf` nginx configuration:
```
upstream thttpd {
    server 127.0.0.1:10000;
    keepalive 16;
}

server {
    server_name shouldiridemuni.com;
    try_files $uri @app;
    location @app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;

        # Enable backend keepalives
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_redirect off;
        proxy_pass http://thttpd;
    }
}
```

`get-mlb-schedule.sh` goes in `/usr/local/sbin` executed via the following crontab in `/etc/cron.d` as `www-data`: 

```
00 00,12 * * * www-data /usr/local/sbin/get-mlb-schedule.sh
```

## License

This work is licensed under CC BY-NC version 4.0 [https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)
© 2022, Josh Enders. Some Rights Reserved.

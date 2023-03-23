# shouldridemuni.com

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## About

I built this site to help make my commute easier during baseball season.

After leaving work in San Francisco's SoMa neighborhood, you're often faced with the question: 

"Should I take the bus or should I take the train?".

The consequences of making the wrong decision on a game day cannot be overstated...

The bus system is usually the slower option but on "Game Days™", it's a TON faster since
out-of-towners (aka Giants fans) simply cannot comprehend the complexity of the Muni
bus system.

Judgemental? Yes. Apologetic? Not at all.

![A point of view shot of a mob of Giants baseball fans rushing into a open traincar door](docs/giants_fans.jpg)

## Performance

The page is optimized for extremely low bandwidth and high latency cellular connections. The whole page
fits in a very conservative TCP MSS of 1380 bytes and is cacheable. Sadly, it's not a use case where you
can ever rely on 0-RTT to speed up TLS, so no https (sorry).

## Improvements

It's currently written in Bash (lol) and runs as a plain old CGI script. It should
probably be rewritten on Cloudflare's Workers platform.

## Installation

Executed via [`thttpd`](https://acme.com/software/thttpd/) as `www-data`

> `/etc/thttpd/thttpd.conf`
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

> `/etc/nginx/sites-available/shouldiridemuni.conf`
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

`get-mlb-schedule.sh` goes in `/usr/local/sbin` executed via the following
crontab in `/etc/cron.d` as `www-data`: 

```
00 00,12 * * * www-data /usr/local/sbin/get-mlb-schedule.sh
```

## License

This work is licensed under CC BY-NC version 4.0 [https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)
© 2023, Josh Enders. Some Rights Reserved.

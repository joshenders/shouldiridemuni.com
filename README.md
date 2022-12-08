# shouldridemuni.com

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## About

I built this site to be used while making split second transit decisions,
often faced with the question: "Should I take the bus or walk to the MUNI
platform for a more direct route home?".

Giants Fans (aka out-of-towners) generally don't understand the bus system in
San Francisco and so what can typically be a more circuitous option ends up
being a lot faster on days there is a home game.

I can't overstate how bad the consequences are if you make the wrong choice...

## Performance

The page is optimized for extremely low cellular bandwidth. The whole page
fits in a very conservative TCP MSS of 1380 bytes. Sadly, I can't count on
0-RTT TLS, so no https (sorry).

## Improvements

It's currently written in Bash and runs as a CGI script. It should probably be
rewritten on Cloudflare's Workers platform.

## Installation

Runs via [https://acme.com/software/thttpd/](`thttpd`)

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

`get-mlb-schedule.sh` goes in `/usr/local/sbin` executed via root's crontab.

## License

This work is licensed under CC BY-NC version 4.0 [https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)
© 2022, Josh Enders. Some Rights Reserved.

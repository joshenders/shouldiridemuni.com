# shouldridemuni.com

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## About

I built this site to help make my commute easier during baseball season.

After leaving work in San Francisco's SoMa neighborhood, you're often faced with the question:

> Should I take the bus home or should I take the train?

The consequences of making the wrong decision on a game day cannot be overstated...

The bus system is generally the slower option but on "Game Days", it's a TON faster since
out-of-towners (aka Giants fans) simply cannot comprehend the complexity of the bus system.

Judgemental? Yes. Apologetic? No. Not at all.

![A point of view shot of a mob of Giants baseball fans rushing into a open traincar door](docs/giants_fans.jpg)

## Performance

The page is optimized for extremely low bandwidth and high latency cellular connections. The whole page
fits in a very conservative TCP MSS of 1380 bytes and is cacheable.

~~Sadly, it's not a use case where you can ever rely on 0-RTT to speed up TLS, so no https (sorry).~~

The world has moved on since I first created this site in 2013 and HTTPS has eaten the world (this is partially my fault but I'm not sorry!). It is now served over HTTPS and ironically, slower and less reliable under high latency conditions. Hopefully, cellular coverage and bandwidth have improved somewhat as well? Mea culpa but we cannot stop the arrow of time now can we?

## Improvements

It's currently written in Bash (lol) and runs as a plain old CGI script. It should probably be rewritten on the Cloudflare's Workers platform.

## Installation

Clone files to `/usr/share/nginx/shouldiridemuni`

```sh
sudo -u www-data git clone https://github.com/joshenders/shouldiridemuni.com /usr/share/nginx/shouldiridemuni
```

Updates can be done with a simple `git pull`:

```sh
sudo git -C /usr/share/nginx/shouldiridemuni.com pull
```

### `thttpd` Configuration

[`thttpd`](https://acme.com/software/thttpd/) is a simple CGI "app server" which will run `index.cgi` for each request.

1. Symlink [`thttpd.conf`](conf/thttpd.conf) to `/etc/thttpd/thttpd.conf`.

    ```sh
    ln -s /usr/share/nginx/shouldiridemuni.com/conf/thttpd.conf /etc/thttpd/thttpd.conf
    ```

2. Symlink [`thttpd.service`](conf/thttpd.service) to `/etc/systemd/system/thttpd.service`.

    ```sh
    ln -s /usr/share/nginx/shouldiridemuni.com/conf/thttpd.service /etc/systemd/system/thttpd.service
    ```

3. Reload systemd and enable and start the service.

    > [!NOTE]
    > [`thttpd`](https://acme.com/software/thttpd/) runs as root and then setuid/setgid/setgroup to `www-data`

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl enable thttpd.service
    sudo systemctl start thttpd.service
    ```

Logs can be viewed with:

```sh
sudo journalctl -u thttpd -f
```

### `nginx` Configuration

Requests are handled by [`nginx`](https://nginx.org) which proxies to `thttpd`.

1. Symlink nginx config fragment [`shouldiridemuni.com](conf/shouldiridemuni.com.conf)` to `/etc/nginx/sites-available/shouldiridemuni.com`

    ```sh
    ln -s /usr/share/nginx/shouldiridemuni.com/conf/shouldiridemuni.com.conf /etc/nginx/sites-available/shouldiridemuni.com
    ```

### MLB cronjob Installation

A cronjob runs a shell script twice a day as `www-data` which populates the games "database" –– a simple `.csv` file in `/usr/share/nginx/shouldiridemuni.com`.

1. Symlink [`get-mlb-schedule.sh`](conf/get-mlb-schedule.sh) to `/usr/local/sbin`.

    ```sh
    ln -s /usr/share/nginx/shouldiridemuni.com/conf/get-mlb-schedule.sh /usr/local/sbin/get-mlb-schedule.sh
    ```

2. Install crontab in `/etc/cron.d`.

    ```sh
    ln -s usr/share/nginx/shouldiridemuni.com/conf/get-mlb-schedule.cron /etc/cron.d/get-mlb-schedule.cron
    ```

3. (Optional) If you don't want to wait 12 hours, you can seed the initial generation of `schedule.csv` with:

    ```sh
    sudo -u www-data  /usr/local/sbin/get-mlb-schedule.sh
    ```

## License

This work is licensed under CC BY-NC version 4.0 [https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)
© 2023, Josh Enders. Some Rights Reserved.

#README
relayctl allows a network connected [Raspberry Pi](https://www.raspberrypi.org/help/what-is-a-raspberry-pi/), a.k.a RPi, to toggle a relay controlled power strip, like the [IoT relay](http://www.digital-loggers.com/iotfaqs.html), whenever you lose internet connectivity. To determine if the RPi has internet connectivity, it pings a list of hosts provided in the configuration. It **assumes** that the relay is **normally closed** (mains power flows when the relay is unenergized).
##Installation Prerequisites
This document assumes that you are running [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) Jessie or Jessie Lite. All command line instructions assume that you are running them on the RPi command line.

On your RPi will need python3, make, pigpio, the pigpio python3 packages, and supervisor. They are available via apt, simply run:
    
    sudo apt-get install python3 make pigpio python3-pigpio supervisor

##Installing relayctl
### Using the provided Makefile
A `Makefile` is provided in the root of the project folder to install relayctl. After installation it will run as a background service via [Supervisor](http://supervisord.org).

First look at the make file so that you understand what it will do (press 'q' to quit):

    less Makefile

Then, if it looked agreeable to you, you can run it with:

    sudo make install

### Running it without installing it

If you want to just run the script you can do that too: run `sudo pigpiod` to start [pigpiod](https://github.com/joan2937/pigpio), then just run relayctl via `python3 relayctl.py [your_config_file]`.  This is great for testing, but you probably want to run it as a service like the `Makefile` creates for you.

###The relayctl user
The relayctl service is configured to use its own unprivileged account.
The makefile adds the user for with the following line: `sudo useradd -r -s /sbin/nologin relayctl`
If for some reason you would perfer not to use the relayctl user, make sure to edit the `supervisor/relayctl.conf` accordingly.
###Configuration
There is a reasonable default configuration provided. The configuration file is a [JSON](https://jsonformatter.curiousconcept.com) document.
Configuration is installed in `/etc/relayctl/relayctl.conf.json`.
  
  * `relay_gpio_bcm`: which [BCM numbered gpio pin](http://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering) to use for relay control. This is the most likely the only value one needs to alter. The default is `17`.
  
  * `consecutive_miss_threshold`: how many consecutive failures to ping any host should be accumulated before toggling the relay. The default is `6`.
  
  * `check_interval_sec`: how long to wait between ping attempts (do not make this unnecessarily short). The default is `10`.
  
  * `power_off_toggle_period_sec`: how long to keep the relay toggled. The default is `10`.
  
  * `post_toggle_quiescence_period_sec`: how long to wait before attempting to ping again after toggling the relay back on. Give your modem and router ample time to reestablish connectivity or you will suffer repeated toggling. The default is set to a reasonable `300`.
  
  * `check_addresses`: a list of addresses to ping. If _any_ of them are reached it is considered a success; see limitations. The default is `["8.8.8.8","8.8.4.4"]`.
  
  * `verbose_logging`: log more information. The default is `true`.
  
###Log files
When running with supervisor the log files will appear in /var/log/supervisor .
One can follow them easily with:

    sudo tail -f /var/log/supervisor relayctl*.log

###Limitations
* Some modems and routers hijack DNS to redirect browsers to a status page when connectivity is lost. relayctl does not check the address that the ping was returned from so it is prone to false positives. For now I recommend only using raw IP addresses and not domain names in `check_addresses`.

* relayctl does not provide for any back off of router restarts

* I don't know if it works with the [PowerTail](http://www.powerswitchtail.com/Pages/default.aspx), I don't see why it wouldn't ... 

* I am not providing physical setup assistance or instructions, play with mains power at your own risk.
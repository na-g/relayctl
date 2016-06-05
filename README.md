#README
##Installing Prerequisites
You will need python3, make, pigpio, the pigpio python3 packages, and supervisor. They are available via apt, simply run:
    
    sudo apt-get install python3 make pigpio python3-pigpio supervisor

##Installing relayctl
### Using the provided Makefile
A makefile is provided in the root of the project folder to install relayctl.
First look at the make file so that you understand what it will do (press 'q' to quit):

    less Makefile

Then, if it looked agreeable to you, you can run it with:

    sudo make install

###The relayctl user
The relayctl service is configured to use its own unprivileged account.
The makefile adds the user for with the following line: `sudo useradd -r -s /sbin/nologin relayctl`
If for some reason you would perfer not to use the relayctl user, make sure to edit the `supervisor/relayctl.conf` accordingly.
###Configuration
There is a reasonable default configuration provided.
Configuration is installed in `/etc/relayctl/relayctl.conf.json`.
  
  * `relay_gpio_bcm`: which gpio pin to use for relay control. This is the most likely the only value one needs to alter. The default is `17`.
  
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
* some modems and routers hijack DNS to redirect browsers to a status page when connectivity is lost. relayctl does not check the address that the ping was returned from so it is prone to false positives. For now I recommend only using raw IP addresses and not domain names in `check_addresses`.

* relayctl does not provide for any back off of router restarts
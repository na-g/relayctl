#!/usr/bin/env python3

import os
import sys
import shlex
import time
import pigpio
import json
import logging
import random

DEFAULT_CONFIGURATION = {
	'relay_gpio_bcm':17,
	'consecutive_miss_threshold':6,
	'check_interval_sec':30,
	'power_off_toggle_period_sec':10,
	'post_toggle_quiescence_period_sec':300,
	'check_addresses':[
		'8.8.8.8',
		'8.8.4.4',
	],
	'verbose_logging':True,
}

cfg = DEFAULT_CONFIGURATION

# Read the configuration if one was provided
if len(sys.argv) == 2:
	print("Reading configuration from: %s"%sys.argv[1])
	with open(sys.argv[1]) as cfg_file:
		cfg = json.load(cfg_file)
elif len(sys.argv) > 2:
	print("Usage: relayctl.py [configuration_file]\n")
	exit(-1)
else:
	print("No configuration file selected, using defaults.")

# Select log level
if cfg['verbose_logging']:
	logging.basicConfig(level=logging.DEBUG)
else:
	logging.basicConfig(level=logging.WARN)

logging.info("Using configuration:")
logging.info(json.dumps(cfg,indent=2))
# Setup the gpio
gpio = pigpio.pi()
gpio.set_mode(cfg['relay_gpio_bcm'], pigpio.OUTPUT)

# Track the number missed in a row
number_missed = 0
try:
	while True:
		time.sleep(cfg['check_interval_sec'])
		logging.debug("Checking for connectivity")
		# Check all hosts for connectivity to _any_ one of them
		contacted_any = False
		hosts = cfg['check_addresses']
		random.shuffle(hosts)
		# Check hosts in random order, stop as soon as there is a success
		for host in hosts:
			if os.system(' '.join(shlex.quote(arg) for arg in ['ping','-c1', host])) == 0:
				logging.debug("Contacted host %s"%host)
				contacted_any = True
				break
			else:
				logging.warn('Unable to contact host %s'%host)
		if contacted_any:
			number_missed = 0
		else:
			logging.warn('Unable to contact any host')
			number_missed = number_missed + 1
		if number_missed >= cfg['consecutive_miss_threshold']:
			logging.warn("%d consecutive failures to contact any host, toggling power to the router."%number_missed)
			number_missed = 0
			# Toggle and hold the relay off for the reset period
			gpio.write(cfg['relay_gpio_bcm'],True)
			time.sleep(cfg['power_off_toggle_period_sec'])
			# Reset the relay
			gpio.write(cfg['relay_gpio_bcm'],False)
			# Give the router long enough to reestablish a connection
			logging.info("Completed toggling power to the router, entering quiescence for %d seconds."%cfg['post_toggle_quiescence_period_sec'])
			time.sleep(cfg['post_toggle_quiescence_period_sec'])
			logging.info('Coming out of quiescence.')
except KeyboardInterrupt:
	print("KeyboardInterrupt")
	gpio.stop()
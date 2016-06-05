.PHONEY:install

install:
	cp relayctl.py /usr/local/sbin/
	# Copy the supervisor configuration
	cp supervisor/conf.d/relayctl.conf /etc/supervisor/conf.d/relayctl.conf
	# Creat a configuration folder and add the default configuration
	mkdir -p /etc/relayctl
	cp configuration/relayctl.conf.json /etc/relayctl/relayctl.conf.json
	# Check for the relayctl user and add if it doesn't exist
	id -u relayctl &>/dev/null || sudo useradd -r -s /sbin/nologin relayctl
	# Make sure that /etc/relayctl is owned by root
	chown -R root /etc/relayctl
	# Make sure that the pigpio daemon will run at boot and start it
	systemctl enable pigpiod
	systemctl start pigpiod
	# Make sure that the supervisor daemon will run at boot and start it
	systemctl enable supervisor
	systemctl start supervisor	
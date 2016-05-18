#!/bin/bash

####################################################
# This file needs to be run when setting up the tortoise for the first time
#
# The watchdog background process is added to .bashrc to be launched
# at startup time.
####################################################


# Directory of this file
BASEDIR=$(dirname `readlink -f $0`)

chmod +x $BASEDIR/lowlevel/watchdog.sh

# If the watchdog is not in the .bashrc file, it is added
if ! grep -Fxq "$BASEDIR/lowlevel/watchdog.sh >/dev/null &" ~/.bashrc
then
        echo  >> ~/.bashrc
        echo "# Only one instance of the weatchdog is created" >> ~/.bashrc
        echo "if [ \`ps aux | grep watchdog.sh | wc -l\` -eq 1 ]" >> ~/.bashrc
        echo "then" >> ~/.bashrc
	echo -e "\t$BASEDIR/lowlevel/watchdog.sh >/dev/null &" >> ~/.bashrc
        echo "fi" >> ~/.bashrc

	source ~/.bashrc
fi

exit 0

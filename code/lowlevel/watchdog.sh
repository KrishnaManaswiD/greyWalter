#!/bin/bash

# Directory of this file
BASEDIR=$(dirname `readlink -f $0`)

PIDS_DIRECTORY=~/.tortoise_pids

# If the directory where the .pid files will be saved doesn't exist, it is created
mkdir -p $PIDS_DIRECTORY

# All .pid files are removed
rm $PIDS_DIRECTORY/*.pid 2>/dev/null

while true
do
    # Counts the number of files .pid in PIDS_DIRECTORY
    N_FILES=`ls -l $PIDS_DIRECTORY/*.pid 2>/dev/null | wc -l`

    # If there are .pid files, it means either the process is running or it has been suddenly stopped
    if [ $N_FILES -gt 0 ]
    then

        for f in $PIDS_DIRECTORY/*.pid
        do
            # Gets PID from file
            PID=`echo $f | cut -d '/' -f 5 | cut -d '.' -f 1`
            echo $PID

            # Looks for PID in list of processes
            EXISTS=`ps aux | awk '{print $2}' | grep $PID | wc -l`

            # If it doesn't exist, it means the process has been stopped
            if [ $EXISTS -eq 0 ]
            then
                MOTOR_PINS=`sed '1!d' $f`
                LED_PINS=`sed '2!d' $f`

		echo "The process doesn't exist. Killing motors pins: $MOTOR_PINS"

                if [ `echo $MOTOR_PINS | wc -w` -eq 8 -a `echo $LED_PINS | wc -w` -eq 4 ]
                then
                        python $BASEDIR/tortoise_cleanup.py $MOTOR_PINS $LED_PINS
                fi

                # Removes the .pid file
                rm $f
            fi
        done
    fi
    
    sleep 1
done





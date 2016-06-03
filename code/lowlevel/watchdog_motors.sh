#!/bin/bash

# TODO: launch script to .bashrc

PIDS_DIRECTORY=~/.tortoise_pids

# If the directory where the .pid files will be saved doesn't exist, it is created
mkdir -p $PIDS_DIRECTORY

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
                echo "The process doesn't exist: KILL MOTORS"

                MOTOR_PINS=`head -n 1 $f`

                # TODO: check current working directory
                python ./tortoise_cleanup.py $MOTOR_PINS

                # Removes the .pid file
                # TODO: uncomment
#                rm $f
            fi

        done

    fi
    
	sleep 1
done





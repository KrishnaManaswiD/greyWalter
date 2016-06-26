#!/bin/bash

if [ -f ./.messages_copy.py ]
then

    cp ./.messages_copy.py ./messages.py

else
    echo "Can't change to wicked mode! No messages_copy.py"
fi

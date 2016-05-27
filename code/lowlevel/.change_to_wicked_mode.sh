#!/bin/bash

if [ -f ./.wicked_messages_copy.py ]
then

    cp ./.wicked_messages_copy.py ./messages.py

else
    echo "Can't change to wicked mode! No wicked_messages_copy.py"
fi

#!/bin/bash
# Your venv path and your python program path. Make sure your python program is executable and your cron job
# user is the same as your playwright installation

LOGGED_USER=$(whoami)
USER_ID=$(id -u "$LOGGED_USER")

export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/${USER_ID}/bus"
export RUNNING_FROM_CRON=1
/home/carl/PycharmProjects/update12SML/.venv/bin/python /home/carl/PycharmProjects/update12SML/src/update12SML.py
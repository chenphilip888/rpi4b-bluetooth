#!/bin/sh
rfkill unblock bluetooth
echo "pairable on\ndiscoverable on\nexit\n" | bluetoothctl

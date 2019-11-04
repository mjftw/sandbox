#!/bin/bash

PKG_NAME=$(basename $(pwd))

echo "Linking $PKG_NAME..."
# Link this package dir into /usr/lib/node_modules
sudo npm link

# Link this package dir into ~/.node-red dir
cd ~/.node-red
npm link $PKG_NAME

# Restart NodeRed server
echo "Restarting NodeRed server..."
sudo service nodered stop
sudo service nodered start

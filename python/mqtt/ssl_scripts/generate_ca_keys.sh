#!/bin/bash
# Generate a CA public private key pair and certificate

if [ -z "$1" ]; then
    echo "Usage: $0 <key duration>"
    exit
fi

DURATION="$1"

openssl req -new -x509 -days $DURATION -extensions v3_ca -keyout ca.key -out ca.crt
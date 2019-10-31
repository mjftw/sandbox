#!/bin/bash
# Install a broker sever private key, certificate, and the CA cert
#   that signed it into mosquitto, and enable SSL on the server

if [ -z "$1" -o -z "$2" -o -z "$3" -o -z "$4" ]; then
    echo "Usage: $0 <ca.cert> <server.cert> <server.key> <mosquitto install dir>"
    exit
fi

CA_CERT="$1"
SERVER_CERT="$2"
SERVER_KEY="$3"
MOSQUITTO_DIR="${4%/}"

if [ ! -e $CA_CERT ]; then
    echo "Error: CA certificate does not exist $CA_CERT"
    exit
fi

if [ ! -e $SERVER_CERT ]; then
    echo "Error: Server certificate does not exist $SERVER_CERT"
    exit
fi

if [ ! -e $SERVER_KEY ]; then
    echo "Error: Server key does not exist $SERVER_KEY"
    exit
fi

if [ ! -d $MOSQUITTO_DIR ]; then
    echo "Error: Mosquitto install dir does not exist $MOSQUITTO_DIR"
    exit
fi

CERTS_DIR="$MOSQUITTO_DIR/certs"
CONF_DIR="$MOSQUITTO_DIR/conf.d"
CONF_FILE="$CONF_DIR/ssl.conf"

# Create certs dir if it does not exist
mkdir -p $CERTS_DIR

# Copy certs and keys
cp $CA_CERT $CERTS_DIR
cp $SERVER_CERT $CERTS_DIR
cp $SERVER_KEY $CERTS_DIR


echo "port 8883" > $CONF_FILE
echo "cafile $CERTS_DIR/$(basename $CA_CERT)" >> $CONF_FILE
echo "certfile $CERTS_DIR/$(basename $SERVER_CERT)" >> $CONF_FILE
echo "keyfile $CERTS_DIR/$(basename $SERVER_KEY)" >> $CONF_FILE
echo "tls_version tlsv1" >> $CONF_FILE

service mosquitto restart

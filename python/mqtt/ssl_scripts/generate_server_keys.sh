#!/bin/bash
# Given an existing CA certificate and CA key pair file
#   create and sign a boker server SSL/TLS key

if [ -z "$1" -o -z "$2" -o -z "$3" ]; then
    echo "Usage: $0 <ca.cert> <ca.private_key> <key duration>"
    exit
fi

CA_CERT="$1"
CA_KEY="$2"
DURATION="$3"

if [ ! -e $CA_CERT ]; then
    echo "Error: CA certificate does not exist $CA_CERT"
    exit
fi

if [ ! -e $CA_KEY ]; then
    echo "Error: CA private key does not exist $CA_KEY"
    exit
fi

# Generate broker key
openssl genrsa -out server.key 2048

# Create certificate signing request
openssl req -out server.csr -key server.key -new

# Sign key with CA certificate
openssl x509 -req -in server.csr -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial -out server.crt -days $DURATION

rm server.csr

mkdir -p for_client
cp $CA_CERT for_client/ca.crt

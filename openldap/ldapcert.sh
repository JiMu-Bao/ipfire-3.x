#!/bin/sh
#
# This is a temporary script to generate a self-signet certificate for the openLDAP service.
#
LDAPCERTDIR=/etc/openldap/certs

# Check if a server key allready exists.
if [ ! -f $LDAPCERTDIR/server.key ]; then
	echo "Generating openLDAP server key."
	openssl genrsa -out $LDAPCERTDIR/server.key 2048

	# Fix ownership and permissions.
	chown ldap:ldap $LDAPCERTDIR/server.key
	chmod 0600 $LDAPCERTDIR/server.key
fi

# Check if the certificate allready exists.
if [ ! -f $LDAPCERTDIR/server.pem ]; then
	echo "Generating CSR"
	openssl req -new -key $LDAPCERTDIR/server.key \
		-out $LDAPCERTDIR/server.csr

	echo "Signing certificate"
	openssl x509 -req -days 365 -in \
		$LDAPCERTDIR/server.csr -signkey $LDAPCERTDIR/server.key \
		-out $LDAPCERTDIR/server.pem

	# Remove unneeded csr file.
	rm -rvf $LDAPCERTDIR/server.csr

	# Fix ownership and file permissions.
	chown ldap:ldap $LDAPCERTDIR/server.pem
	chmod 0600 $LDAPCERTDIR/server.pem
fi

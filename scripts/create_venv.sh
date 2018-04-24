# SPDX-License-Identifier: Apache-2.0
#

#!/bin/bash -eu

if [ ! -d venv ]; then
		virtualenv venv;
	fi

if ! which configtxgen
	then
		if  [ ! -e fabric-bin/bin/configtxgen ];
		then
			echo "configtxgen doesn't exits."
			mkdir -p fabric-bin
			(cd fabric-bin && curl -sSL https://goo.gl/6wtTN5 | bash -s -- -d -s) #downloads only binary
			if [ $? -gt 0 ];
			then
				echo "Binary download failed."
				exit 1
			fi
		fi
		cp fabric-bin/bin/configtxgen venv/bin/configtxgen
	fi
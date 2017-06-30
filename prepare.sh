#!/bin/bash

for program in unzip tidy; do
	which $program 2>&1 >/dev/null
	if [[ $? != 0 ]]; then
		echo "Required program missing: $program" 1>&2
		exit 1
	fi
done

FACEBOOK_EXPORT=$1

if [ ! -f "$FACEBOOK_EXPORT" ]; then
	echo "It looks like $FACEBOOK_EXPORT isn't a Facebook account export." 1>&2
	exit 1
fi

EXPORT_MESSAGES_PATH="html/messages.htm"
echo "Trying to extract $EXPORT_MESSAGES_PATH from $FACEBOOK_EXPORT"

set -x
unzip -p "$FACEBOOK_EXPORT" "$EXPORT_MESSAGES_PATH" | tidy > "messages.html" 2> "prepare.log"

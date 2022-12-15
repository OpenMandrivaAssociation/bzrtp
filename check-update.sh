#!/bin/sh
curl "https://github.com/BelledonneCommunications/bzrtp/tags" 2>/dev/null |grep "tag/" |sed -e 's,.*tag/,,;s,\".*,,;' |grep -E '^[0-9.]+$' |grep -v '[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]' |sort -V |tail -n1


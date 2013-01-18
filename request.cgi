#!/bin/bash
# БЕЗН0ГNМ СКРИПТ
source config.cgi

echo -e "Content-type: text/html;charset=utf-8\n"

echo "<html>"
echo "<head>"
echo "<title>request page</title>"
echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://anoos.tk/root.css\">"
echo "</head>"
echo "<body>"

if [ $ENABLE_REQUEST -eq '1' ]
then
	ARTIST=$(echo $QUERY_STRING | sed -n 's/^.*artist=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
	ARTIST=$(echo $ARTIST | echo -e $(sed 's/%/\\x/g'))
	TITLE=$(echo "$QUERY_STRING" | sed -n 's/^.*title=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | echo -e $(sed 's/%/\\x/g'))
	TITLE=$(echo $TITLE | echo -e $(sed 's/%/\\x/g'))
	LINK=$(echo "$QUERY_STRING" | sed -n 's/^.*link=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | echo -e $(sed 's/%/\\x/g'))
	LINK=$(echo $LINK | echo -e $(sed 's/%/\\x/g'))
	NAME=$(echo "$QUERY_STRING" | sed -n 's/^.*name=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | echo -e $(sed 's/%/\\x/g'))
	NAME=$(echo $NAME | echo -e $(sed 's/%/\\x/g'))
	ip=$(/bin/env | grep REMOTE_ADDR | cut -f 2 -d"=")
	check_wiper=$(cat $REQUEST_WIPE_FILE | grep $ip)

	if [ -n "$ARTIST" ] || [ -n "$TITLE" ]
	then
		if [ -n "$check_wiper" ]
		then
			wipe_time=$(echo $check_wiper | cut -f 2 -d" ")
			current_time=$(date "+%s")
			let "time=$current_time - $wipe_time"

			if [ $time -lt $REQUEST_WAIT_TIME ]
			then
				let "seconds=$REQUEST_WAIT_TIME-$time"
				echo Анон, ты сможешь услать реквест только через $seconds секунд
				exit
			fi

			sed "s/$ip\ $wipe_time/$ip\ $current_time/" $REQUEST_WIPE_FILE > $REQUEST_WIPE_FILE".tmp"
			mv $REQUEST_WIPE_FILE".tmp" $REQUEST_WIPE_FILE
		else
			echo "$ip $(date '+%s')" >> $REQUEST_WIPE_FILE
		fi
	else
		echo Обязательно нужно указать artist и title
		exit
	fi

	echo Малаца, хорошо, что среквестировал
	echo -e "Song: $ARTIST - $TITLE\nLink: $LINK\nName: $NAME\nIP: $ip" | sendxmpp -s REQUEST -f $XMPP_CONF deanon@deanon.tk
	echo -en "[Request]\nSong:$ARTIST - $TITLE\nLink: $LINK" | sendxmpp -f $XMPP_CONF -c radio@conference.deanon.tk 
else
	echo $DISABLE_REQUEST_MESSAGE
fi

echo "</body>"
echo "</html>"

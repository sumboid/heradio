#!/bin/bash

source config.cgi

echo -e "Content-type: text/html;charset=utf-8\n"

echo "<html>"
echo "<head>"
echo "<title>ls page</title>"
echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://anoos.tk/root.css\">"
echo "</head>"
echo "<body>"
if [ $ENABLE_LS -eq '1' ]
then
	QUERY_STRING=$(echo $QUERY_STRING | echo -e $(sed 's/%/\\x/g'))
	ip=$REMOTE_ADDR

	if expr "$QUERY_STRING" : '.*\(mp3\|m4a\|flac\|ogg\|wav\)$' > /dev/null;
	then
		if [ $ENABLE_ADD -eq '1' ]
		then
			check_wiper=$(cat $LS_WIPE_FILE | grep $ip)
			if [ -n "$check_wiper" ]
			then
				wipe_time=$(echo $check_wiper | cut -f 2 -d" ")
				current_time=$(date "+%s")
				let "time=$current_time - $wipe_time"
				if [ $time -lt $LS_WAIT_TIME ]
				then
					let "seconds=$LS_WAIT_TIME-$time"
					echo Анон, ты сможешь добавить трек только через $seconds секунд
					exit
				fi
				sed "s/$ip\ $wipe_time/$ip\ $current_time/" $LS_WIPE_FILE > $LS_WIPE_FILE".tmp"
				mv $LS_WIPE_FILE".tmp" $LS_WIPE_FILE
			else
				echo "$ip $(date '+%s')" >> $LS_WIPE_FILE
			fi

			echo Трек добавлен в очередь

			mpc -h $MPD_PASS@$MPD_HOST add "$QUERY_STRING"
			echo -en "$QUERY_STRING\n IP: $ip" | sendxmpp -s ADD -f $XMPP_CONF deanon@deanon.tk 
			echo -en "[Add from local library]\n$QUERY_STRING" | sendxmpp -f $XMPP_CONF -c radio@conference.deanon.tk 


		else
			echo $DISABLE_ADD_MESSAGE
		fi
	fi
else
	echo $DISABLE_LS_MESSAGE
fi
echo "</body>"
echo "</html>"

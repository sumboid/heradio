#!/bin/bash

source config.cgi

echo -e "Content-type: text/html;charset=utf-8\n"

./start-html.cgi
echo "</head>"
echo "<body>"

QUERY_STRING=$(echo $QUERY_STRING | cut -f 1 -d"&")
QUERY_STRING=$(echo $QUERY_STRING | echo -e $(sed 's/%/\\x/g'))
QUERY_STRING=$(echo $QUERY_STRING | cut -f 2 -d"=")

if [[ "http://radio.deanon.tk/koka.png" == "$QUERY_STRING" ]]
then
	echo "<center><h1>Положи Коку на место!</h1></center>"
	exit
fi

if [ $ENABLE_UPLOAD -eq '1' ]
then
	echo "<h1>Стоит дождаться сообщения о добавлении трека.</h1>"

	link=$(curl "$QUERY_STRING" 2>/dev/null | grep -m 1 "http://rghost.\(net\|ru\)/.*\.\(mp3\|flac\|ogg\|MP3\|FLAC\)"  | cut -f 2- -d"$(echo -e "\"")" | cut -f 1 -d"$(echo -e "\"")")
	ip=$REMOTE_ADDR

	track_time=$(curl "$QUERY_STRING" 2>/dev/null |  grep -A 2 "\(Duration\|Длина:\)" | sed '$!d' | grep '\(^[0-9] мин.*\|^[0-9]* с\)')

	if [ "$link" ]
	then
		if [ "$track_time" ]
		then
			check_wiper=$(cat $UPLOAD_WIPE_FILE | grep $ip)
			if [ -n "$check_wiper" ]
			then
				wipe_time=$(echo $check_wiper | cut -f 2 -d" ")
				current_time=$(date "+%s")
				let "time=$current_time - $wipe_time"
				if [ $time -lt $UPLOAD_WAIT_TIME ]
				then
					let "seconds=$UPLOAD_WAIT_TIME-$time"
					echo Анон, ты сможешь добавить трек только через $seconds секунд
					exit
				fi
				sed "s/$ip\ $wipe_time/$ip\ $current_time/" $UPLOAD_WIPE_FILE > $UPLOAD_WIPE_FILE".tmp"
				mv $UPLOAD_WIPE_FILE".tmp" $UPLOAD_WIPE_FILE
			else
				echo "$ip $(date '+%s')" >> $UPLOAD_WIPE_FILE
			fi

			error=$(curl -I "$link" 2>/dev/null | grep "HTTP/1.1 302 Found")
			if [ "$error" ]
			then
				direct_link=$(curl -I $link 2> /dev/null| grep Location | cut -f 2- -d":" | cut -c 2- | cut -f 1 -d"$(echo -e "\r")")
			else
				direct_link=$link
			fi
			#content_type=$(curl -I $direct_link 2> /dev/null| grep "Content-Type" | cut -f 2 -d":" | cut -f 1 -d"/" | cut -c 2- | cut -f 1 -d"$(echo -e "\r")")
			#if [[ "audio" == $content_type ]]
			#then
				current_time=$(date "+%s")
				echo "<p>Downloading</p>"
				wget $direct_link -O $UPLOAD_DIR/$current_time.mp3
				mpc -h $MPD_PASS@$MPD_HOST update --wait > /dev/null
				mpc -h $MPD_PASS@$MPD_HOST add "$UPLOAD_PATH/$current_time.mp3" 2>&1
				echo -e "File:$QUERY_STRING\nFilename:$current_time.mp3\nIP: $ip" | sendxmpp -s UPLOAD -f $XMPP_CONF yoba@ 
				echo -en "[Add from rghost]\n$QUERY_STRING" | sendxmpp -f $XMPP_CONF -c radio@conference.deanon.tk 
				echo "<p>Трек добавлен в очередь</p>"
			#else
			#	echo "<p>Анус свой обманывай, пёс</p>"
			#	exit
			#fi
		else 
			echo "<p>Слишком большая длина трека (больше 9 минут 59 секунд)</p>"
		fi
	else
		echo "<p>Не музыка вовсе</p>"
	fi
else
	echo $DISABLE_UPLOAD_MESSAGE
fi
echo "</body>"
echo "</html>"

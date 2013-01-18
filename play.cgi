#!/bin/bash

source config.cgi

echo -e "Content-type: text/html; charset: utf-8\n"

./start-html.cgi

echo "<title>play</title>"
echo "</head>"
echo "<body>"
echo "<center>"

if [ $ENABLE_PLAY -eq '1' ]
then
	/usr/local/bin/startmpd > /dev/null
	echo "<h1>Плеер запущен</h1>"
else
	echo $DISABLE_PLAY_MESSAGE
fi

echo "</center>"
echo "</body>"
echo "</html>"

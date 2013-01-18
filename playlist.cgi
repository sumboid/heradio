#!/bin/bash
source config.cgi
echo -e "Content-type: text/html; charset=utf-8\n"

# our html code
echo "<table class=\"table table-hover table-condensed\">"
if [ $ENABLE_PLAYLIST -eq "1" ]
then
	echo "<tr><th>Artist</th><th>Title</th><th>Album</th><th>Time</th></tr>"
	current=`mpc -h $MPD_PASS@$MPD_HOST current -f "<td>%artist%</td><td>%title%</td><td>%album%</td><td>%time%</td>"`
	mpc -h $MPD_PASS@$MPD_HOST playlist -f "<td>%artist%</td><td>%title%</td><td>%album%</td><td>%time%</td>" | 
	while read line;
	do
		echo -n "<tr"

		if test "$line" = "$current" 
		then
			echo -en " class=\"info\""
		fi

		echo -n ">"
		echo -e "$line</tr>"
	done
fi
echo "</table>"

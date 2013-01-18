#!/bin/bash

source config.cgi
echo -e "Content-type: text/html; charset=utf-8\n"

./start-html.cgi

echo "<title>radio</title>"
echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://anoos.tk/borders.css\">"
echo "<script type=\"text/JavaScript\">"
echo "function refresh(){ location.reload(true); }"
echo "</script>"
cat << EOF
		<script>
			function fucking_play(){
				document.getElementById("play").style.display = "none";
				document.getElementById("stop").style.display = "block";
				document.getElementById('player').play();
			}
		</script>
EOF
echo "</head>"
echo "<body>"

if [ $ENABLE_PLAYLIST -eq "1" ]
then
	listeners=`curl http://anoos.tk:8000 -s | grep "Current Listeners" -A 1 | sed '$!d' | cut -f 2 -d'>' | cut -f 1 -d'<'`

	if [ $listeners ]
	then
		echo "<div class=\"block\">"
		echo "<p class=\"pblock\">Radio:</p>"
		#echo "<p>Current listeners: $listeners</p>"
		cat player.inc
		echo "</div>"
	else
		echo "<p>Radio is not available</p>"
	fi
else
	echo "<p>Radio is not available</p>"
fi

echo "</body>"
echo "</html>"

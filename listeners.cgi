#!/bin/bash
source config.cgi
echo -e "Content-type: text/html; charset=utf-8\n"

# our html code
echo "<html>"
echo "<head>"
echo "<title>Playlist page</title>"
echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://anoos.tk/root.css\">"
echo "<script type=\"text/JavaScript\">"
echo "function refresh(time){ setTimeout(\"location.reload(true);\", time); }"
echo "</script>"
echo "</head>"
echo "<body onload=\"JavaScript:refresh(2000);\">"
echo -n "Listeners: "
echo $(curl http://anoos.tk:8000 -s | grep "Current Listeners" -A 1 | sed '$!d' | cut -f 2 -d'>' | cut -f 1 -d'<')
echo "</body></html>"

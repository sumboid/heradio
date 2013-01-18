#!/bin/sh

source config.cgi

t()
{
	while IFS= read l;do
		printf "\t%s\n" "$l";
	done
}

link_enc() {
	sed -e 's/%/%25/g' -e 's/ /%20/g' -e 's/!/%21/g' -e 's/"/%22/g' -e 's/#/%23/g' -e 's/\$/%24/g' -e 's/\&/%26/g' -e 's/'\''/%27/g' -e 's/(/%28/g' -e 's/)/%29/g' -e 's/\*/%2a/g' -e 's/+/%2b/g' -e 's/,/%2c/g' -e 's/-/%2d/g' -e 's/\./%2e/g' -e 's/\//%2f/g' -e 's/:/%3a/g' -e 's/;/%3b/g' -e 's//%3e/g' -e 's/?/%3f/g' -e 's/@/%40/g' -e 's/\[/%5b/g' -e 's/\\/%5c/g' -e 's/\]/%5d/g' -e 's/\^/%5e/g' -e 's/_/%5f/g' -e 's/`/%60/g' -e 's/{/%7b/g' -e 's/|/%7c/g' -e 's/}/%7d/g' -e 's/~/%7e/g';
}

#'`} # fix buggy vim syntax

xml_enc()
{
	sed -e 's/</&lt;/g' -e 's/&/&amp;/g'
}

w()
{
	printf "%s\n" "$1"
}

l()
{
	
	if mpc -h $MPD_PASS@$MPD_HOST ls "$1" 2>/dev/null >/dev/null
	then
		local S
		[ $N -ne 0 ] && S=1
		[ $S ] &&
		{
			text="$(xml_enc <<< "$1" |awk -F/ '{print $NF}')"
			w "<a class='directory' href='#' onclick=\"dir_show_hide('dir_$N');return false\">$text</a><br/>"
			w "<div class='dir' id='dir_$N'>"
		}
		((N++))

		while IFS= read line;do
			l "$line"
		done < <(mpc -h $MPD_PASS@$MPD_HOST ls  "$1")
		[ $S ] && w "</div>"
	else
		href="$(link_enc <<< "$1")"
		text="$(xml_enc <<< "$1" |awk -F/ '{print $NF}')"
		w "<a class='track' href='ls?$href'>$text</a><br/>"
	fi
}

cat << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<link rel="stylesheet" type="text/css" href="http://anoos.tk/root.css"/>
		<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
		<title>ls and add</title>
		<script type="text/javascript">
			function dir_show_hide(id)
			{
				var d = document.getElementById(id).style;
				if(d.display != "block")
					d.display = "block";
				else
					d.display = "none";
			}
		</script>
	</head>
	<body>
		<div>
EOF

N=0
l /|t|t|t

cat << EOF
		</div>
	</body>
</html>
EOF

exit 0

if [ ! -n  "$1" ]
then
	mpc -h $MPD_PASS@$MPD_HOST ls  |
	while read line;
	do
		./$0 "$line"
	done
	exit
fi



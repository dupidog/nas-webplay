#! /bin/bash

echo "Content-type: text/html"
echo ""

ROOTDIR="/var/smbshare/video"
SUBROOTDIR="/"

mkdir -p links

[ "$QUERY_STRING" = "" ] && QUERY_STRING="L:$SUBROOTDIR"

METHOD=${QUERY_STRING:0:1}
URL=${QUERY_STRING:2}
URL=${URL#/}
URL=$(echo $URL | urldecode)

CNT=1
while :; do  
    split=`echo $URL | cut -d "/" -f $CNT`
    if [ ! -z "$split" ]; then
        eval "PARENT${CNT}=\"$split\""
        CNT=$(($CNT+1))
        [ "$split" = "$URL" ] && break
    else
        break
    fi
done

if [ "$METHOD" = "L" ]; then
    eachlink=""
    echo "Current: / <a href=\"?L:\">HOME</a>"
    for each in `seq $CNT`; do
        eachname=`eval echo '$PARENT'"$each"`
        [ -z "$eachname" ] && break
        eachlink="$eachlink/$eachname"
        echo "/ <a href=\"?L:$eachlink\">$eachname</a>"
    done
    echo "<br><br>"
    ls -1 "$ROOTDIR/$URL" | while read each; do
        if [ -f "$ROOTDIR/$URL/$each" ]; then
            echo "<a href=\"?P:$URL/$each\">$each</a><br>"
        elif [ -d "$ROOTDIR/$URL/$each" ]; then
            echo "<a href=\"?L:$URL/$each\">$each</a><br>"
        fi
    done 
elif [ "$METHOD" = "P" ]; then
    templink=$(echo $RANDOM$RANDOM$RANDOM | md5sum | cut -d ' ' -f 1)
    ln -s "$ROOTDIR/$URL" "links/$templink.mp4"
    echo '<script type="text/javascript" src="jwplayer.js"></script>
          <script type="text/javascript">jwplayer.key="UfxDNzKyqowO5F2rMS0JkhfqvKNNT8Zz/Ra/nw==";</script>

          <div id="myElement">Loading the player...</div>

          <script type="text/javascript">
          jwplayer("myElement").setup({
          file: ' "\"links/$templink.mp4\"" ',
          image: "/uploads/myPoster.jpg"
          });
          </script>'
fi

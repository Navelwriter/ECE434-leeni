# here's how to use imagemagick to display text
# make a blank image
size=320x240
source=borisRotate.png
TMP_FILE=temp.png


# from: http://www.imagemagick.org/usage/text/
convert "$source" -pointsize 42 \
    label:'Noah Lee' +swap -append \
    -resize "$size" "$TMP_FILE"

sudo fbi -noverbose -T 1 $TMP_FILE
# Clean up the temporary files
rm $TMP_FILE

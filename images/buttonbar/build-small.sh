rm *-small.png

for file in *.png
do
    newfile=`echo $file | sed 's/\(.*\)\.png/\1-small.png/'`
    convert $file -resize 100x100 $newfile
done
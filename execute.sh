#!/bin/bash
input_files=`find input -name "*.jpg"`
for file in $input_files
do
	file=`echo $file | awk -F "input/" '{print $2}'`
	out=`echo $file | awk -F "." '{print $1}'`
	out="output/"$out".json"
	echo "Processing $file and redirected to $out"
	curl -XGET "https://tvzdzzak83.execute-api.us-east-1.amazonaws.com/dev/get-text?file-name=$file" |  python -m json.tool >> $out
done

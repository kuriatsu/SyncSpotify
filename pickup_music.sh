#!/bin/zsh

# usage : ./pickup_music.sh <music_dir> <dap_dir>
dap_dir=$2
pickup_num=100

# clear data
rm $dap_dir/*.mp3

files=()
while read file; do
	files+=(${file})
done < <(ls $1)

for i in $(seq 0 ${#files[@]} | shuf | head -n $pickup_num); do
	cp "$1/$files[$i]" $dap_dir
done


#!/bin/bash
base_dir=$1
out_dir=""
while read path; do
    file=${path#*${base_dir}}
    output_file="${out_dir}/${file%.flac}.mp3"
    echo " $path > $output_file"
    if [ ! -e "${path}" ]; then
        echo "${path} not exist"
        continue
    fi
    if [ -e "$output_file" ]; then
        echo "${output_file} exist"
        continue
    fi

    ffmpeg -i "${path}" -c:a mp3 -vn -b:a 192k "${output_file}" < /dev/null
    #    echo $output_file
    sleep 1
done < <(find $base_dir -name *.flac)

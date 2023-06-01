#!/bin/bash

#Please change NODE_NAME, MEMCACHE_PORT, FILENAME value respectively
# connect to memcached
exec 3<>/dev/tcp/"${1:-NODE_NAME}"/"${2:-MEMCACHE_PORT}" || exit $? 

# get slab numbers
printf 'stats slabs\r\n' >&3
slabnums=()
while IFS=' :' read -r stat slabnum _; do
    if [[ $stat == $'END\r' ]]; then
        break
    fi
    if ! [[ $slabnum =~ ^[0-9]*$ ]]; then
        continue
    fi
    for index in "${!slabnums[@]}"; do
        if [[ ${slabnums[index]} == "$slabnum" ]]; then
            continue 2
        fi
    done
    slabnums+=($slabnum)
done <&3
# dump each slab
outfile="FILENAME"
for ((index=0;index<${#slabnums[@]};index++)); do
    slabnum=${slabnums[index]}
    printf 'stats cachedump %d 0\r\n' "$slabnum" >&3
    while read -r line; do
        if [[ $line == $'END\r' ]]; then
            break
        fi
        printf '%d: %s\n' "$slabnum" "${line%$'\r'}" >> "$outfile"
    done <&3
done
# close connection
printf 'quit\r\n' >&3
exec 3<&-

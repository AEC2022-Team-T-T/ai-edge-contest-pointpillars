#!/usr/bin/env bash

function usage {
	echo './switch_dataset.sh <dataset>
	dataset: should be one of the "public" or "contest"'
}

function switch_to_public {
	rm data/nuscenes && ln -s /mnt/fsx/public/nuscenes/data/ data/nuscenes
}

function switch_to_contest {
	rm data/nuscenes && ln -s /mnt/fsx/public/ai-edge-contest/train/3d_labels/ data/nuscenes
}

if [[ "$#" -lt 1 || -z $1 ]]; then
	usage
	exit 1
fi

dataset=$1

tools_dir="$(dirname "$(realpath "$0")")"
cd ${tools_dir}/../

if [[ ${dataset} == "public" ]]; then
	switch_to_public
elif [[ ${dataset} == "contest" ]]; then
	switch_to_contest
else
	usage
	exit 1

fi

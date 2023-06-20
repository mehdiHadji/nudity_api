#!/bin/bash

echo "####### Stop all containers..."
sudo docker kill $(sudo docker ps -q)

echo "####### Remove all containers..."
sudo docker rm $(sudo docker ps -a -q)

echo "####### Remove all images..."
sudo docker rmi -f $(sudo docker images -q)

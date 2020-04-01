#!/bin/bash

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116

sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 67170598AF249743

sudo sh -c 'echo "deb [arch=amd64] http://jderobot.org/apt xenial main" > /etc/apt/sources.list.d/gazebo-stable.list'
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 24E521A4

sudo apt update

sudo apt install jderobot-gazebo-assets -y
sudo apt install gazebo -y
sudo apt install ros-kinetic-desktop-full -y
sudo apt-get install python-pip -y
sudo pip2 install git+https://github.com/jupyter/kernel_gateway.git
sudo pip2 install numpy
sudo apt install libjansson-dev nodejs npm nodejs-legacy libboost-dev imagemagick libtinyxml-dev mercurial cmake build-essential

cd ~; hg clone https://bitbucket.org/osrf/gzweb
cd ~/gzweb
hg up gzweb_1.4.0
source /usr/share/gazebo/setup.sh
source /opt/ros/kinetic/setup.bash
source /opt/jderobot/share/jderobot/gazebo/gazebo-assets-setup.sh
npm run deploy --- -m local

export JDEROBOT_SIMULATION_TYPE="LOCAL"
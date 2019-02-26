# Planet Learning

Exoplanet detection ML project

## Installation processes

In order to have everything working properly (on Ubuntu with intel x86x64 CPU and nvidia GPU), follow the installation steps detailed, and taking into account the remarks below :
* For Docker : https://docs.docker.com/install/linux/docker-ce/ubuntu/
* For Tensorflow : https://www.tensorflow.org/install/docker
* For Keras : https://keras.io/

Remarks : 
* Please ensure the use of Python 3.x everywhere
    * For Tensorflow, please use this image : `docker pull tensorflow/tensorflow:latest-py3` 

To verify the installation process :
* for Tensorflow, use : `docker run -u $(id -u):$(id -g) -it tensorflow/tensorflow:latest-py3 bash`

## Launch




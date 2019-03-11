# Planet Learning

Exoplanet detection machine learning academic project, using [TensorFlow](https://www.tensorflow.org/) module Keras and running on [Docker](https://www.docker.com/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### A note on hardware

This project was developped on computers running *Ubuntu 18.04*, with *Intel x86* CPUs and *Nvidia* GPUs. The following steps are detailed for these settings in mind, but can surely be adapted to match with other configurations.

### Prerequisites

Before hand, you need to have the following packages installed on your computer : 

* Docker : for installation processes, please follow the instructions given in the [official documentation](https://docs.docker.com/install/linux/docker-ce/ubuntu/), including the *manage docker as a non-root user* post-installation part detailed [here](https://docs.docker.com/install/linux/linux-postinstall/).
* Docker-compose : for installation processes, please follow the instructions given in the [official documentation](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

You will also need a specific docker image of Tensorflow, which you can install by two different means.

#### Installing Tensorflow docker image from the image built for this project

This method uses the Tensorflow image we built from the repositories, following the steps details [here](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/docker).

You can get this image by pulling from our dockerhub repository : 

```sh
docker pull proxyma/planet-learning:latest-py3
```

#### Installing Tensorflow docker image by building a new one

Should you want to build you own Tensorflow image, you can do so by doing these steps :

```sh
git clone https://github.com/tensorflow/tensorflow
cd tensorflow/tensorflow/tools/docker/

export TF_DOCKER_BUILD_IS_DEVEL=NO
export TF_DOCKER_BUILD_TYPE=CPU
export TF_DOCKER_BUILD_PYTHON_VERSION=PYTHON3

pip download --no-deps tf-nightly

export TF_DOCKER_BUILD_CENTRAL_PIP=$(ls tf_nightly*.whl)
export TF_DOCKER_BUILD_CENTRAL_PIP_IS_LOCAL=1

tensorflow/tools/docker/parameterized_docker_build.sh
```
Please note that we provide those steps to ease the process, but the oficial documentation of Tensorflow is the reference on this matter : you can find it [here](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/docker)

You can then push your newly built image to Dockerhub by following the instructions provided [here](https://docs.docker.com/docker-hub/repos/)

#### Testing the installation of the prerequisites

Should you want to test out the prerequisite packages installation, you can run a version of MNIST problem using the image of Tensorflow previously downloaded / built.

The MNIST problem files are available [here](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/tutorials/mnist).

To test it, run these commands in a terminal : 

```sh
docker run -it --rm -v $PWD:/tmp -w /tmp user/name-of-repo:tag python ./hello_world.py
```

With ```user/name-of-repo``` being the name of your Dockerhub repo, for example : 

```sh
docker run -it --rm -v $PWD:/tmp -w /tmp proxyma/planet-learning:latest-py3 python ./hello_world.py
```

### Installing

To install the project, clone it : 

```sh
git clone git@gitlab.viarezo.fr:Wanysteus/planet-learning.git
```

In order to make it run on [TESS](https://fr.wikipedia.org/wiki/Transiting_Exoplanet_Survey_Satellite) data, you need to download it from [here](http://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html).

### Running

In order to test out the project, run into a terminal :

```sh
docker-compose build
docker-compose up
```

Please note that the outputted URL in the terminal for [Tensorboard]() is not correct : should you want to access to the Tensorboard associated with the project, access it from localhost http://0.0.0.0:6006/.
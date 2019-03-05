# Planet Learning

Exoplanet detection ML project

## Installation processes

In order to have everything working properly (on Ubuntu with intel x86x64 CPU and nvidia GPU), follow the installation steps detailed, and taking into account the remarks below :
* For Docker : https://docs.docker.com/install/linux/docker-ce/ubuntu/
* For Tensorflow : https://www.tensorflow.org/install/docker
* For Keras : it is already inside of the TensorFlow package

Remarks : 
* Please ensure the use of Python 3.x everywhere
    * For Tensorflow, please use this image : 
    ```sh 
    docker pull tensorflow/tensorflow:latest-py3
    ```

To verify the installation process :
* for Tensorflow, use : 
```sh
docker run -u $(id -u):$(id -g) -it tensorflow/tensorflow:latest-py3 bash
```
## Launch

To launch a script (for instance here an hello-world script) :

```sh
docker run -it --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow:latest-py3 python ./hello_world.py
```

##  Build the official docker images for tensorflow

Clone `https://github.com/tensorflow/tensorflow`

Go to `tensorflow/tensorflow/tools/docker/`

```sh
export TF_DOCKER_BUILD_IS_DEVEL=NO
export TF_DOCKER_BUILD_TYPE=CPU
export TF_DOCKER_BUILD_PYTHON_VERSION=PYTHON3

pip download --no-deps tf-nightly

export TF_DOCKER_BUILD_CENTRAL_PIP=$(ls tf_nightly*.whl)
export TF_DOCKER_BUILD_CENTRAL_PIP_IS_LOCAL=1

tensorflow/tools/docker/parameterized_docker_build.sh
```

You can get the created image by pulling from dockerhub

```sh
docker pull proxyma/planet-learning:latest-py3
```

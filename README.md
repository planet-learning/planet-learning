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



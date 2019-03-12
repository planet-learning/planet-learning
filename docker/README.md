# Docker configuration for Planet Learning

Documentation of the docker(-compose) configuration for the project.
## Tree of files

There is two Dockerfiles for the project, one for the tensorboard service, another running the project's code

```
── docker
   ├── README.md
   ├── code
   │   └── Dockerfile
   └── tensorboard
       └── Dockerfile
```

## Note when using custom images

If you elected to use your own built custom image of Tensorflow in docker, that you put in your Dockerhub, please note that you need to update the `FROM` statement used in the Dockerfiles.
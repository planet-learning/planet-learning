# Pulls our image from the repo
FROM proxyma/planet-learning:latest-py3

LABEL Name=planet-learning Version=0.0.1

#Expose port for Tensorboard
EXPOSE 6006

#setting the working directory and adding access to the data
WORKDIR /planet-learning
ADD . /planet-learning

# Pip-install of the requirements, if any:
RUN python3 -m pip install -r requirements.txt

#Running of the code
CMD ["python3", "-m", "hello_world_with_summaries"]

#Launching Tensorboard
CMD ["tensorboard", "--logdir=/planet-learning/tensorflow/mnist/logs"]

#TO-DO
# s'occuper du port forwarding pour tensorboard
# avoir accès au code
# avoir accès aux données


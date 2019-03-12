# Pulls our image from the repo
FROM proxyma/planet-learning:latest-py3

LABEL Name=planet-learning-tensorboard Version=0.0.1

#Expose port for Tensorboard
EXPOSE 6006

#setting the working directory and adding access to the data
WORKDIR /planet-learning
COPY requirements.txt /planet-learning/

# Pip-install of the requirements, if any:
RUN python3 -m pip install -r requirements.txt

#Launching Tensorboard
CMD ["tensorboard", "--logdir=/planet-learning/tensorflow/mnist/logs"]
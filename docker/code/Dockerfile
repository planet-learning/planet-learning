# Pulls our image from the repo
# Please change this line if using another custom image of Tensorflow you built
FROM proxyma/planet-learning:latest-py3

LABEL Name=planet-learning-code Version=0.0.1

#setting the working directory and adding access to the data
WORKDIR /planet-learning
COPY requirements.txt /planet-learning/

# Pip-install of the requirements, if any:
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "-m", "extractic/extractic.py"]
# Pulls our image from the repo
# Please change this line if using another custom image of Tensorflow you built
FROM proxyma/planet-learning:latest-py3

LABEL Name=planet-learning-code Version=0.0.1

#Installing wait-for-it script, allowing for waiting on the database to startup
RUN apt-get update && apt-get install -y git
WORKDIR /
RUN git clone https://github.com/vishnubob/wait-for-it.git

#setting the working directory and adding access to the data
WORKDIR /planet-learning/code
COPY requirements.txt /planet-learning/code

# Pip-install of the requirements, if any:
RUN python3 -m pip install -r requirements.txt

#Running the program
CMD ["/wait-for-it/wait-for-it.sh", "planet-learning-database:5432", "--", "python3", "-u","-m",  "planet-learning.main"]

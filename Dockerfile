# set the base image
FROM python:3.9-slim-buster

# set the working directory
WORKDIR /app

# copy the requirements file
COPY requirements.txt .

# install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy the source code
COPY . .

# set the environment variables
ENV FLASK_APP app.py
ENV FLASK_ENV production

# expose the port
EXPOSE 5000

# start the server
CMD ["flask", "run", "--host", "0.0.0.0"]
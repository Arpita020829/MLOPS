# pull the python image from docker hub
# use a lightweight Python imaage
FROM python:3.14-slim

# set the working directory inside container
WORKDIR /app

# copy dependencies list before copying application code
COPY requirements.txt .

# install the dependencies
RUN pip install -r requirements.txt

# copy application code and saved model inside /app
COPY . . 

# document the port used by the FAST API application
EXPOSE 8000

#Start the API server when container is ready
# 0.0.0.0 = allows connection through the container's network interface
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
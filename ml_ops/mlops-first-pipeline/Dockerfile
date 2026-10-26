# pull the python image from docker hub 
#use a lightweight version of python
FROM python:3.14-slim

# set the working directory in the container
WORKDIR /app

# copy the dependencies fefore copying the source code to leverage Docker cache
COPY requirements.txt .


RUN pip install -r requirements.txt

# copy application code and saved model inside /app
COPY . .

# document the port used by the FastAPI app
EXPOSE 8000

# Start api server when the container starts
# 0.0.0.0 - allows connections through the conainer's newtork interface
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
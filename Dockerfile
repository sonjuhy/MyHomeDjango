# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt ./

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

ARG DATABASE_PASSWORD
ARG DATABASE_USER
ARG DATABASE_NAME
ARG DATABASE_PORT
ARG DATABASE_HOST
ARG SECRET_KEY
ENV DATABASE_PASSWORD=$DATABASE_PASSWORD
ENV DATABASE_USER=$DATABASE_USER
ENV DATABASE_NAME=$DATABASE_NAME
ENV DATABASE_PORT=$DATABASE_PORT
ENV DATABASE_HOST=$DATABASE_HOST
ENV SECRET_KEY=$SECRET_KEY


# Run the application on the poart 8000
EXPOSE 8000

# Specify the command to run when the container starts
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000", "--noreload" ]
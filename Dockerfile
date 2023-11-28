# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt ./

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Run the application on the poart 8000
EXPOSE 8000

# Specify the command to run when the container starts
CMD [ "python", "./manage.py", "runserver", "--noreload" ]
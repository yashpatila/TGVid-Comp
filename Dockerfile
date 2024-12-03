# Use the official Python image as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg fontconfig && \
    rm -rf /var/lib/apt/lists/*

# Copy the app's code into the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set executable permissions for the run script
RUN chmod +x run.sh

# Specify the command to run the application
CMD ["bash", "run.sh"]

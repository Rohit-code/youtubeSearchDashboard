# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR D:\Users\bonir\Documents\GitHub\youtubeSearchDashboard

# Copy the current directory contents into the container at /app
COPY . /D:/Users/bonir/Documents/GitHub/youtubeSearchDashboard

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME youtubeSearchDashboard

# Run app.py when the container launches
CMD ["python", "app.py"]

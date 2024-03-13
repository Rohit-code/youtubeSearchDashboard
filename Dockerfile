# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /YoutubeSearchDashboard

# Copy the current directory contents into the container at /app
COPY . /YoutubeSearchDashboard

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME youtubeSearchDashboard

# Run app.py when the container launches
CMD ["python", "YoutubeSearchDashboard/manage.py","runserver", "0.0.0.0:8000"]

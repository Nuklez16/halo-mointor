# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the script into the container
COPY halo_server_check.py /app/

# Install Flask
RUN pip install flask

# Expose port 5000
EXPOSE 5000

# Run the script
CMD ["python", "/app/halo_server_check.py"]

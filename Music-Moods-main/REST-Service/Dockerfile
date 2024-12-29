# Use Python base image
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Copy requirements file first to install dependencies
COPY ./REST-Service/requirements.txt /app/

# Install dependencies
RUN pip install  -r requirements.txt

# Copy all application files to the container
COPY ./ /app/

# Expose the REST service port
EXPOSE 8001

# Command to run the REST service with Uvicorn (adjust to your app setup)
CMD ["uvicorn", "Rest:app", "--host", "127.0.0.1", "--port", "8001"]

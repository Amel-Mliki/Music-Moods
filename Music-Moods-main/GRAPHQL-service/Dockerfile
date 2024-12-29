# Use Python base image
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Copy requirements file first to install dependencies
COPY ./GRAPHQL-service/requirements.txt /app/


RUN pip install cython

# Install dependencies
RUN pip install -r requirements.txt

# Copy all application files to the container
COPY ./ /app/

# Expose the GraphQL service port
EXPOSE 8002

# Command to run the GraphQL service with Uvicorn
CMD ["uvicorn", "GraphQL:app", "--host", "127.0.0.1", "--port", "8002"]

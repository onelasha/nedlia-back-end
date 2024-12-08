#!/bin/bash

# Get the environment from command line argument, default to development
ENV=${1:-development}

# Copy the appropriate .env file
echo "Setting up $ENV environment..."
cp .env.$ENV .env

# Install dependencies based on environment
if [ "$ENV" = "development" ]; then
    pip install -r requirements/dev.txt
elif [ "$ENV" = "test" ]; then
    pip install -r requirements/test.txt
else
    pip install -r requirements/prod.txt
fi

# Start the application
echo "Starting application in $ENV mode..."
python -m app

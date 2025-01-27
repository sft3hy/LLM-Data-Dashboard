# Start from Python base image
FROM python:3.10-slim-bullseye


# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
   build-essential \
   libpq-dev \
   gdal-bin \
   libgdal-dev \
   libgeos-dev \
   && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
# Set the working directory in the container
WORKDIR /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port for Streamlit
EXPOSE 8501

# Command to run your app (if applicable)
CMD ["streamlit", "run", "st_app.py"]






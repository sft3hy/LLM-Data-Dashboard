# Start from Python 3.11 Alpine
FROM python:3.11-slim


# Install system dependencies needed for Python packages
RUN apk update && apk add --no-cache \
   gdal \
   geos \
   proj \
   && pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app


# Copy your application files into the container
COPY . /app


# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port for Streamlit
EXPOSE 8501

# Command to run your app (if applicable)
CMD ["streamlit", "run", "st_app.py"]






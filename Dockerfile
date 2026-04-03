# Use an official Python image
FROM python:3.9-slim

# Set the 'home' folder inside the container
WORKDIR /app

# Copy your files from your PC into the container
COPY . /app

# Run the installation inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Tell the container which port to open
EXPOSE 5000

# The command to start the app
CMD ["python", "app.py"]
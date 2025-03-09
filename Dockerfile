# Use an official lightweight Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the current directory into /app
COPY . /app/

# Ensure Python recognizes `utils/` as a package
RUN mkdir -p /app/utils && touch /app/utils/__init__.py

# Install dependencies
RUN pip install --no-cache-dir flask beautifulsoup4 requests gunicorn

# Expose the Flask port
EXPOSE 8080

# Start the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "message_generator.app:app"]

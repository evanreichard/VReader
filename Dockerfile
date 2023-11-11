# Build Container
FROM python:3.11-slim

# Install App
WORKDIR /app
COPY . /app

# Install App & Gunicorn
RUN pip install .
RUN pip3 install gunicorn

# Cleanup
RUN rm -rf /app

# Start Application
ENTRYPOINT ["gunicorn"]
EXPOSE 5000
CMD ["vreader:create_app()", "--bind", "0.0.0.0:5000", "--threads=4", "--access-logfile", "-"]

# retextai_test_task

Usage: 
touch .env && echo SECRET_KEY=YOUR_SECRET_KEY > .env && docker-compose up -d

Implemented:
- Docker-compose file for building the project in a single command
- Asynchronous task queue using Celery
- Message broker - Redis
- Flask application for document translation
- NGINX for serving static files and reducing the load on the WSGI server
- WSGI server (Gunicorn) for running the Flask application
- AJAX requests for asynchronous file processing
- Checking the validity of the file content before downloading to the host and processing.

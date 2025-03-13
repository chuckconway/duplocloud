FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random

# Set environment variables for Node.js installation
ENV NODE_VERSION=23.x

# Install necessary dependencies for adding a new repository and fetching packages over HTTPS
RUN apt-get update && \
    apt-get install -y curl gnupg2 ca-certificates software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Add Node.js PPA (Personal Package Archive)
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash -

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y nodejs build-essential

# Optionally, you can clean up to reduce image size
RUN rm -rf /var/lib/apt/lists/*

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY uv.lock pyproject.toml requirements.txt /code/

# Install Python dependencies
# For some reason, uv sync wasn't working.
# RUN uv pip freeze > requirements.txt
RUN pip install -r requirements.txt

# Creating folders, and files for a project:
COPY . /code

WORKDIR /code/src/client
RUN npm install
RUN npm run build

WORKDIR /code/src/documents/duplocloud/application-focussed-interface
RUN ls

WORKDIR /code

EXPOSE 8897

# previous attempts. Keeping for reference.
#CMD ["gunicorn", "-b", "0.0.0.0:8897", "src.app:app"]
#CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8897"]

# Not ideal command. We should be using gunicorn or uvicorn. A better web server that supports socketio is FastAPI and is compatiable with uvicorn.
CMD ["python", "-m", "src.app", "--host", "0.0.0.0", "--port", "8897", "--allow_unsafe_werkzeug"]
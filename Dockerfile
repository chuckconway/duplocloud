FROM python:3.13.2-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # ^^^
  # Make sure to update it!

# System deps:

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY uv.lock pyproject.toml /code/

# Project initialization:


# Creating folders, and files for a project:
COPY . /code

EXPOSE 8897

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8897"]
FROM python:3.11.12-slim

# turn off pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# paths for running poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.6.1
ENV PATH="$PATH:$POETRY_HOME/bin"

# Turn off buffering for logging purposes
ENV PYTHONUNBUFFERED 1

# Install and setup poetry
RUN pip install -U pip \
    && apt-get update \
    && apt install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 -


RUN apt-get install libgdal-dev -y



# Set the working directory
WORKDIR /src
# copy needed files to container
COPY pyproject.toml poetry.lock ./

COPY . .

# install python dependencies with poetry
RUN poetry install --no-interaction --no-ansi



EXPOSE 8001

# Set the environment variable for Flask
ENV BASE_APP_DIRECTORY=/src/app
ENV BASE_APP_NAME=NebraskaRasterQueries

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
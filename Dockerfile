FROM python:3.9

# build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev

# Web app source code
COPY . /app
WORKDIR /app

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN wget -O - https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && poetry --version \
    && poetry config virtualenvs.create false

# TODO: Add --no-dev conditionally for production
RUN poetry install --no-interaction --no-ansi -vvv

EXPOSE 3031

CMD [ "uwsgi", "--http", "0.0.0.0:3031", \
               "--protocol", "uwsgi", \
               "--wsgi", "app:app" ]

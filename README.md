# Codenames Backend

Backend for an implementation of the Codenames boardgame

## Dependencies

You must have these installed before running

- [python 3.6+](https://www.python.org/)
- [poetry](https://python-poetry.org/)

## Quickstart

1. Install libraries

    ```bash
    poetry install
    ```

2. Create a copy of the `.env` file from the supplied template and edit as required

    ```bash
    cp template.env .env
    ```

3. Initialise the database

    ```bash
    poetry run flask db upgrade head
    ```

4. Run the development server

    ```bash
    poetry run flask run
    ```

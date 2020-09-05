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

4. Populate the database with some words

    ```bash
    poetry run python load_words.py --new-langauge --language=EN data/words/words_en.txt
    ```

    You can use the `load_words.py` script to load files with more words and languages. For info on how to use it, run

    ```bash
    poetry run python load_words.py --help
    ``` 

5. Run the development server

    ```bash
    poetry run flask run
    ```

6. If using VS Code, do the following to use the right virtual environment

    ```bash
    poetry shell
    code .
    ```

    Then select the correct virtual environment with the `Python: Select Interpreter` command
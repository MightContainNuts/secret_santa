FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install --upgrade poetry

# Install dependencies without dev dependencies
RUN poetry install --no-interaction --without dev --verbose

# Copy the rest of the application code
COPY . /app/

# Set the default command for the container
CMD ["poetry", "run", "python", "secret-santa.py"]

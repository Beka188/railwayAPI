FROM python:3.11 as requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.0
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY /Users/lawliet/NFactorial/hw-backend-6-Beka188/app/main.py /code

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

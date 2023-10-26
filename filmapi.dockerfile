FROM python:3.11-slim
WORKDIR /code
COPY ./ /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["uvicorn", "film_api:app", "--host", "0.0.0.0", "--port", "8000"]

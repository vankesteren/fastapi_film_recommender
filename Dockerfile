FROM python:3.11-slim
# Install postgres and set up db
RUN apt install postgresql-12
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "-c", "import polars as pd; print(pd.DataFrame({'hello': 1}))"]
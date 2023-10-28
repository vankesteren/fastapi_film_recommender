FROM postgres:alpine
RUN wget https://raw.githubusercontent.com/xzilla/pagila/master/pagila-schema.sql -O /docker-entrypoint-initdb.d/1_schema.sql
RUN wget https://raw.githubusercontent.com/xzilla/pagila/master/pagila-data.sql -O /docker-entrypoint-initdb.d/2_data.sql

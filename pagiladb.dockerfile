FROM postgres:alpine
RUN apk add curl
RUN curl https://raw.githubusercontent.com/xzilla/pagila/master/pagila-schema.sql -o /docker-entrypoint-initdb.d/1_schema.sql
RUN curl https://raw.githubusercontent.com/xzilla/pagila/master/pagila-data.sql -o /docker-entrypoint-initdb.d/2_data.sql

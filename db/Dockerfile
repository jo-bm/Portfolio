FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=testdb

COPY ./sql-scripts/ /docker-entrypoint-initdb.d/

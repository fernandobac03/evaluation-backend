
FROM postgres:9.6
MAINTAINER Open Knowledge

# Customize default user/pass/db
#ENV POSTGRES_USER ckan
#ENV POSTGRES_PASSWORD ckan
#ENV POSTGRES_DB ckan

# Install DataStore
RUN ls /var/lib/postgresql
RUN chmod +x /var/lib/postgresql
COPY /initDatabase.sh /docker-entrypoint-initdb.d/


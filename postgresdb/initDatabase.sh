psql -U postgres -c "CREATE ROLE ucuenca WITH PASSWORD 'ucuenca2017'"
psql -U postgres -c "CREATE DATABASE geolinkeddata owner ucuenca"
psql -U postgres -c "ALTER ROLE ucuenca WITH LOGIN"
export PGPASSWORD=ucuenca2017 
psql geolinkeddata -U ucuenca -c "CREATE TABLE personas (id DOUBlE PRECISION PRIMARY KEY, escuela VARCHAR(200) NOT NULL, edad INTEGER NOT NULL, genero VARCHAR(5) NOT NULL)" 
psql geolinkeddata -U ucuenca -c "CREATE TABLE pares (id SERIAL PRIMARY KEY, uri_a VARCHAR(1000), uri_b VARCHAR(1000))"
psql geolinkeddata -U ucuenca -c "CREATE TABLE evaluacion (id SERIAL PRIMARY KEY, evaluacion VARCHAR(5), id_persona DOUBLE PRECISION, id_par INTEGER)"






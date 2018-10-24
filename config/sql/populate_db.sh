#!/bin/bash
set -e

psql --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE digitalmarketplace;
	CREATE DATABASE digitalmarketplace_test;
EOSQL
psql --username="$POSTGRES_USER" --dbname="digitalmarketplace" -f /docker-entrypoint-initdb.d/data/*.sql

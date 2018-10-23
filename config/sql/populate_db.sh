#!/bin/bash
set -e

psql -d postgresql://localhost:5432 -c 'create database digitalmarketplace;'
psql -d postgresql://localhost:5432/digitalmarketplace -c 'create database digitalmarketplace_test;'
psql -d postgresql://localhost:5432/digitalmarketplace -f /docker-entrypoint-initdb.d/data/*.sql

#!/bin/bash

HOST=http://localhost:8000
NUMBER_TABLES=$((1 + RANDOM % 10))

poetry run python src/simulation -t "$NUMBER_TABLES" --host "$HOST"

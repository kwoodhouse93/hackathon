#!/bin/bash
COMPOSE_OPTIONS="-f docker-compose.yml -f production.yml"
docker-compose $COMPOSE_OPTIONS down \
    && docker-compose $COMPOSE_OPTIONS build \
    && docker-compose $COMPOSE_OPTIONS up -d

#!/bin/bash

MANAGE=/home/precise/repo/bonifacio/backend/manage.py

echo "Engineering Fixtures"

echo "Loading building categories..."
python $MANAGE loaddata building_categories.json

echo "Loading co statuses..."
python $MANAGE loaddata co_statuses.json

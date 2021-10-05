#!/bin/bash

MANAGE=/home/precise/repo/bonifacio/backend/manage.py

echo "PPB Fixtures"

echo "Loading expense classes..."
python $MANAGE loaddata expense_classes.json

echo "Loading object codes..."
python $MANAGE loaddata object_codes.json

echo "Loading mission areas..."
python $MANAGE loaddata mission_areas.json

echo "Loading kmas..."
python $MANAGE loaddata kmas.json

echo "Loading major paps..."
python $MANAGE loaddata major_paps.json

echo "Loading sub paps..."
python $MANAGE loaddata sub_paps.json

echo "Loading suggested paps..."
python $MANAGE loaddata suggested_paps.json

#!/bin/bash

MANAGE=/home/precise/repo/bonifacio/backend/manage.py

echo "Mobility Fixtures"

echo "Loading categories..."
python $MANAGE loaddata categories.json

echo "Loading tonnages..."
python $MANAGE loaddata tonnages.json

echo "Loading types..."
python $MANAGE loaddata types.json

echo "Loading nomenclature vehicles..."
python $MANAGE loaddata nomenclature_vehicles.json

echo "Loading vehicle records..."
python $MANAGE loaddata vehicle_records.json

echo "Loading nomenclature tires..."
python $MANAGE loaddata nomenclature_tires.json

echo "Loading nomenclature batteries..."
python $MANAGE loaddata nomenclature_batteries.json

#!/bin/bash

MANAGE=/usr/src/app/manage.py

echo "Commons Fixtures"

echo "Loading organizations..."
python $MANAGE loaddata organizations.json

echo "Loading roles..."
python $MANAGE loaddata roles.json

echo "Loading pamus..."
python $MANAGE loaddata pamus.json

echo "Loading units..."
python $MANAGE loaddata units.json

echo "Loading regions..."
python $MANAGE loaddata regions.json

echo "Loading procurement modes..."
python $MANAGE loaddata procurement_modes.json

echo "Loading acquisition modes..."
python $MANAGE loaddata acquisition_modes.json

echo "Loading serviceabilities..."
python $MANAGE loaddata serviceabilities.json

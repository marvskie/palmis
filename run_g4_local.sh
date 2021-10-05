#!/bin/bash

MANAGE=/home/precise/repo/bonifacio/backend/manage.py

workon narra
python $MANAGE runserver 190.168.1.23:8000

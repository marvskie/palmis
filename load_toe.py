import os
import json

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narra.settings')
django.setup()

from tosb.models import *

mapping = {
    'mba': 'Military Body Armor',
    'armrack': 'Armrack',
    'binocular': 'Binocular',
    'compass': 'Compass',
    'cot_bed': 'Cot Bed',
    'foam': 'Foam',
    'ftt': 'Frame Type Tent',
    'fuel_tanker': 'Fuel Tanker',
    'helmet': 'Helmet',
    'parachute': 'Parachute',
    'steel_bed': 'Steel Bed',
    'towable': 'Towable'
}

use_ats = 'foam'

for key, value in mapping.items():
    with open(f'TOE/{key}.json', 'r') as jfile:
        oe = OrgEquipment.objects.create(name=value)
        data = json.load(jfile)

        for item in data:
            u = item['unit'].strip()
            p = item['pamu'].strip()
            if not p or not u:
                continue

            try:
                pamu = Pamu.objects.get(name__iexact=p)
            except Pamu.DoesNotExist:
                pamu = Pamu.objects.create(name=p)

            try:
                unit = Unit.objects.get(name__iexact=u, pamu=pamu)
            except Unit.DoesNotExist:
                unit = Unit.objects.create(name=u, pamu=pamu)

            if item['toe']:
                _ = Toe.objects.create(unit=unit, oe=oe, toe=item['toe'])

            if item['baseline']:
                _ = Baseline.objects.create(unit=unit, oe=oe, baseline=item['baseline'], active=True)

            if key == use_ats:
                _ = Ats.objects.create(unit=unit, ats=item['ats'])

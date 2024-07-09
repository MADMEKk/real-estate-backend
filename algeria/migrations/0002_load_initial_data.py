from django.db import migrations
import json
import os

def load_initial_data(apps, schema_editor):
    Wilaya = apps.get_model('algeria', 'Wilaya')
    Daira = apps.get_model('algeria', 'Daira')
    Commune = apps.get_model('algeria', 'Commune')

    # Load JSON data
    json_path = os.path.join(os.path.dirname(__file__), '..', 'algeria_cities.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            wilaya, created = Wilaya.objects.get_or_create(
                code=item['wilaya_code'],
                defaults={
                    'name_ascii': item['wilaya_name_ascii'],
                    'name': item['wilaya_name']
                }
            )

            daira, created = Daira.objects.get_or_create(
                name_ascii=item['daira_name_ascii'],
                wilaya=wilaya,
                defaults={'name': item['daira_name']}
            )

            Commune.objects.update_or_create(
                id=item['id'],
                defaults={
                    'name_ascii': item['commune_name_ascii'],
                    'name': item['commune_name'],
                    'daira': daira
                }
            )

class Migration(migrations.Migration):

    dependencies = [
        ('algeria', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]

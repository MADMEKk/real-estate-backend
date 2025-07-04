# Generated by Django 5.0.3 on 2024-03-19 06:16

import django.db.models.deletion
import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("properties", "0003_propertyrequest_remove_property_country_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Agentcontact",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100, verbose_name="Your Name")),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default="+123456789",
                        max_length=30,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("message", models.TextField(verbose_name="Message")),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="properties.property",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

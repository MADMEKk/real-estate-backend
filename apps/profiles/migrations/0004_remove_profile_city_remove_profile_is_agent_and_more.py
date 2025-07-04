# Generated by Django 5.0.3 on 2024-07-02 09:37

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_remove_profile_country"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="city",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="is_agent",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="is_buyer",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="is_seller",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="license",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="num_reviews",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="rating",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="top_agent",
        ),
        migrations.AddField(
            model_name="profile",
            name="firstname",
            field=models.CharField(
                default="firstname", max_length=50, verbose_name="First Name"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="lastname",
            field=models.CharField(
                default="lastname", max_length=50, verbose_name="Last Name"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="naissance",
            field=models.DateField(blank=True, null=True, verbose_name="Date of Birth"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female")],
                default="Male",
                max_length=20,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                default="+1234566789",
                max_length=30,
                region=None,
                verbose_name="Phone Number",
            ),
        ),
    ]

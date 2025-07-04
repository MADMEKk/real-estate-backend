# Generated by Django 5.0.3 on 2024-03-19 06:16

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Propertyrequest",
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
                (
                    "title",
                    models.CharField(max_length=250, verbose_name="Property Title"),
                ),
                (
                    "ref_code",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        unique=True,
                        verbose_name="Property Reference Code",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        default="Default description...update me please....",
                        verbose_name="Description",
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        default="Oran", max_length=180, verbose_name="City"
                    ),
                ),
                (
                    "postal_code",
                    models.CharField(
                        default="140", max_length=100, verbose_name="Postal Code"
                    ),
                ),
                (
                    "street_address",
                    models.CharField(
                        default="USTO", max_length=150, verbose_name="Street Address"
                    ),
                ),
                (
                    "property_number",
                    models.IntegerField(
                        default=112,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Property Number",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=8,
                        verbose_name="Price",
                    ),
                ),
                (
                    "tax",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.15,
                        help_text="15% property tax charged",
                        max_digits=6,
                        verbose_name="Property Tax",
                    ),
                ),
                (
                    "plot_area",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=8,
                        verbose_name="Plot Area(m^2)",
                    ),
                ),
                (
                    "total_floors",
                    models.IntegerField(default=0, verbose_name="Number of floors"),
                ),
                ("bedrooms", models.IntegerField(default=1, verbose_name="Bedrooms")),
                (
                    "bathrooms",
                    models.DecimalField(
                        decimal_places=2,
                        default=1.0,
                        max_digits=4,
                        verbose_name="Bathrooms",
                    ),
                ),
                (
                    "advert_type",
                    models.CharField(
                        choices=[
                            ("For Sale", "For Sale"),
                            ("For Rent", "For Rent"),
                            ("Auction", "Auction"),
                        ],
                        default="For Sale",
                        max_length=50,
                        verbose_name="Advert Type",
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("House", "House"),
                            ("Apartment", "Apartment"),
                            ("Office", "Office"),
                            ("Warehouse", "Warehouse"),
                            ("Commercial", "Commercial"),
                            ("Other", "Other"),
                        ],
                        default="Other",
                        max_length=50,
                        verbose_name="Property Type",
                    ),
                ),
                (
                    "cover_photo",
                    models.ImageField(
                        blank=True,
                        default="/house_sample.jpg",
                        null=True,
                        upload_to="",
                        verbose_name="Main Photo",
                    ),
                ),
                (
                    "photo1",
                    models.ImageField(
                        blank=True,
                        default="/interior_sample.jpg",
                        null=True,
                        upload_to="",
                    ),
                ),
                (
                    "photo2",
                    models.ImageField(
                        blank=True,
                        default="/interior_sample.jpg",
                        null=True,
                        upload_to="",
                    ),
                ),
                (
                    "photo3",
                    models.ImageField(
                        blank=True,
                        default="/interior_sample.jpg",
                        null=True,
                        upload_to="",
                    ),
                ),
                (
                    "photo4",
                    models.ImageField(
                        blank=True,
                        default="/interior_sample.jpg",
                        null=True,
                        upload_to="",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="property",
            name="country",
        ),
        migrations.AddField(
            model_name="property",
            name="photo10",
            field=models.ImageField(
                blank=True, default="/interior_sample.jpg", null=True, upload_to=""
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="photo5",
            field=models.ImageField(
                blank=True, default="/interior_sample.jpg", null=True, upload_to=""
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="photo6",
            field=models.ImageField(
                blank=True, default="/interior_sample.jpg", null=True, upload_to=""
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="photo7",
            field=models.ImageField(
                blank=True, default="/interior_sample.jpg", null=True, upload_to=""
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="photo8",
            field=models.ImageField(
                blank=True, default="/interior_sample.jpg", null=True, upload_to=""
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="photo9",
            field=models.ImageField(
                blank=True, default="/interior_sample.jpg", null=True, upload_to=""
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="vedio",
            field=models.FileField(
                blank=True, default="/interior_sample.jpg", null=True, upload_to=""
            ),
        ),
    ]

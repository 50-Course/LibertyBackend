# Generated by Django 5.0.7 on 2024-07-22 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(help_text="Description of the item")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["name", "price"], name="name_price_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="Product category, e.g groceries, scents, gadgets",
                        max_length=100,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_category",
                        to="core.product",
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-30 03:11

from django.db import migrations

def add_plse(apps, schema_editor):
    Address = apps.get_model('expunger', 'Address')
    address = Address(street1="1501 Cherry Street", city="Philadelphia", state="PA",
            zipcode="19102")
    address.save()

    Organization = apps.get_model('expunger', 'Organization')
    org = Organization(name="Philadelphia Lawyers for Social Equity",
                       phone="215-995-1230", address=address)
    org.save()

    
class Migration(migrations.Migration):

    dependencies = [
        ('expunger', '0002_address_attorney_expungerprofile_organization'),
    ]

    operations = [
        migrations.RunPython(add_plse),
    ]

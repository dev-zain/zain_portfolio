# Generated migration for cv field change to cv_url

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='cv',
        ),
        migrations.AddField(
            model_name='profile',
            name='cv_url',
            field=models.URLField(blank=True, help_text='Link to CV (Google Drive, Dropbox, etc.)'),
        ),
    ]

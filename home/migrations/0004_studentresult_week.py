# Generated by Django 4.1.5 on 2023-02-13 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_student_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresult',
            name='week',
            field=models.CharField(choices=[('FIRST', 'First'), ('SECOND', 'Second'), ('THIRD', 'Third'), ('FOUR', 'Four'), ('FIVE', 'FiVE'), ('SIX', 'Six'), ('SEVEN', 'Seven'), ('EIGHT', 'Eight'), ('NINE', 'Nine'), ('TEN', 'Ten'), ('ELEVEN', 'Eleven'), ('TWELVE', 'Twelve')], max_length=20, null=True),
        ),
    ]

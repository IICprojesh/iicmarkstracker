# Generated by Django 4.1.5 on 2023-02-13 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('course_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SessionYearModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_start_year', models.DateField()),
                ('session_end_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('section', models.CharField(max_length=4)),
                ('email', models.CharField(default='no email', max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.courses')),
            ],
        ),
        migrations.CreateModel(
            name='YearSemester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('ONE', 'One'), ('TWO', 'Two'), ('THREE', 'Three')], max_length=15)),
                ('sem', models.CharField(choices=[('FIRST', 'First'), ('SECOND', 'Second')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.courses')),
                ('term', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.yearsemester')),
            ],
        ),
        migrations.CreateModel(
            name='Studentresult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.subjects')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='year_sem',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.yearsemester'),
        ),
    ]
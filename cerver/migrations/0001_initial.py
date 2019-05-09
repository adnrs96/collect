# Generated by Django 2.2.1 on 2019-05-09 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('total_questions', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FormResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_response_stored', models.BooleanField(default=False)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='cerver.Form')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qheadline', models.CharField(max_length=150)),
                ('qdescription', models.CharField(blank=True, max_length=500)),
                ('question_type', models.PositiveSmallIntegerField(choices=[(1, 'Input text to answer'), (2, 'Input an Integer to answer'), (3, 'Select from True/False')], default=1)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_questions', to='cerver.Form')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=1000)),
                ('form_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='cerver.FormResponse')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='cerver.Question')),
            ],
            options={
                'unique_together': {('form_response', 'question')},
            },
        ),
        migrations.CreateModel(
            name='FormOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_register_id', models.PositiveSmallIntegerField(default=0)),
                ('phase_type', models.PositiveSmallIntegerField(choices=[(1, 'Operation(s) executes on validation stage before any response is stored.'), (2, 'Operation(s) executes immediately after storage is successful.'), (3, 'Operation(s) Triggered by specific command and executes on Response Collective')], default=3)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='cerver.Form')),
            ],
            options={
                'unique_together': {('form', 'operation_register_id')},
            },
        ),
    ]

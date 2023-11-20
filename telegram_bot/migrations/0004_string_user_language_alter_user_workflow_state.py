# Generated by Django 4.2.6 on 2023-11-20 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0003_context_delete_workflowitem_alter_user_telegram_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='String',
            fields=[
                ('string_id', models.CharField(db_index=True, max_length=32, primary_key=True, serialize=False)),
                ('lang_ru', models.TextField()),
                ('lang_en', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(default='ru', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='workflow_state',
            field=models.CharField(max_length=32, null=True),
        ),
    ]

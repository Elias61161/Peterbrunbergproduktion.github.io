# Generated by Django 3.1.7 on 2021-04-29 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('website', '0012_auto_20210418_0123'), ('website', '0013_remove_contentobjectbase_component'), ('website', '0014_auto_20210425_1600'), ('website', '0015_auto_20210429_1945')]

    dependencies = [
        ('website', '0011_backend-content-object-tree-selector_20210411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttext',
            name='text',
            field=models.TextField(blank=True, default='', verbose_name='text'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='contentobjectbase',
            name='component',
        ),
        migrations.AlterField(
            model_name='contentobjectbase',
            name='containing_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.page', verbose_name='containing page'),
        ),
        migrations.AlterField(
            model_name='contentobjectbase',
            name='containing_page',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='website.page', verbose_name='containing page'),
            preserve_default=False,
        ),
    ]

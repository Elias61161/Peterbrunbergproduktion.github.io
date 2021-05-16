# Generated by Django 3.1.7 on 2021-05-16 18:10

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import website.models.redirects


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True, verbose_name='URL')),
                ('page_type', models.CharField(max_length=255, verbose_name='page type')),
                ('published', models.BooleanField(default=False, verbose_name='is published')),
                ('first_published_at', models.DateField(blank=True, null=True, verbose_name='first published at')),
                ('publish_time', models.DateTimeField(blank=True, null=True, verbose_name='publish time')),
                ('unpublish_time', models.DateTimeField(blank=True, null=True, verbose_name='unpublish time')),
                ('last_edited_at', models.DateTimeField(auto_now=True, verbose_name='last edited at')),
            ],
            options={
                'verbose_name': 'base page',
                'verbose_name_plural': 'base pages',
            },
        ),
        migrations.CreateModel(
            name='ContentObjectBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, verbose_name='name')),
                ('db_type', models.CharField(blank=True, choices=[('text', 'text'), ('image', 'image'), ('menu', 'menu'), ('page', 'page'), ('list', 'list'), ('dict', 'dict')], max_length=5, verbose_name='database type')),
                ('attributes', jsonfield.fields.JSONField(blank=True, default='{}', verbose_name='attributes')),
                ('order', models.PositiveSmallIntegerField(blank=True, db_index=True, default=0, verbose_name='order')),
                ('containing_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.basepage', verbose_name='containing page')),
            ],
            options={
                'verbose_name': 'base content object',
                'verbose_name_plural': 'base content objects',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='image')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'image',
            },
        ),
        migrations.CreateModel(
            name='MenuItemBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('url', models.URLField(blank=True, default=None, null=True, verbose_name='url')),
                ('order', models.PositiveSmallIntegerField(blank=True, db_index=True, default=0, null=True, verbose_name='order')),
                ('is_menu', models.BooleanField(verbose_name='is menu')),
            ],
            options={
                'verbose_name': 'base menu item',
                'verbose_name_plural': 'base menu items',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ContentCollection',
            fields=[
                ('contentobjectbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.contentobjectbase')),
                ('is_ordered', models.BooleanField(default=False, verbose_name='is ordered')),
            ],
            options={
                'verbose_name': 'content collection',
                'verbose_name_plural': 'content collections',
            },
            bases=('website.contentobjectbase',),
        ),
        migrations.CreateModel(
            name='ContentText',
            fields=[
                ('contentobjectbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.contentobjectbase')),
                ('text', models.TextField(blank=True, verbose_name='text')),
            ],
            options={
                'verbose_name': 'text content object',
                'verbose_name_plural': 'text content objects',
            },
            bases=('website.contentobjectbase',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.basepage')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug')),
                ('author', models.CharField(blank=True, max_length=255, verbose_name='created by')),
                ('views', models.IntegerField(default=0, verbose_name='views')),
            ],
            options={
                'verbose_name': 'news',
                'verbose_name_plural': 'news',
            },
            bases=('website.basepage',),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.basepage')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Slug')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='website.page', verbose_name='parent page')),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
                'unique_together': {('name', 'parent'), ('slug', 'parent')},
            },
            bases=('website.basepage',),
        ),
        migrations.AddField(
            model_name='basepage',
            name='content_en',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='website_basepage_page_en', to='website.contentobjectbase', verbose_name='english content'),
        ),
        migrations.AddField(
            model_name='basepage',
            name='content_sv',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='website_basepage_page_sv', to='website.contentobjectbase', verbose_name='swedish content'),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
            ],
            options={
                'verbose_name': 'menu',
                'verbose_name_plural': 'menus',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('website.menuitembase',),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
            ],
            options={
                'verbose_name': 'menu item',
                'verbose_name_plural': 'menu items',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('website.menuitembase',),
        ),
        migrations.CreateModel(
            name='ContentCollectionList',
            fields=[
                ('contentcollection_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.contentcollection')),
            ],
            options={
                'verbose_name': 'content collection list',
                'verbose_name_plural': 'content collection lists',
            },
            bases=('website.contentcollection',),
        ),
        migrations.CreateModel(
            name='SiteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root_url', models.URLField(verbose_name='root URL')),
                ('api_root_url', models.URLField(verbose_name='API root URL')),
                ('banner_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='banner_content', to='website.contentcollection', verbose_name='banner content')),
                ('footer_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='footer_content', to='website.contentcollection', verbose_name='footer content')),
                ('root_page', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='website.page', verbose_name='root page')),
            ],
            options={
                'verbose_name': 'site manager',
                'verbose_name_plural': 'site manager',
            },
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_path', models.CharField(max_length=255, unique=True, validators=[website.models.redirects.from_path_validator], verbose_name='from path')),
                ('url', models.URLField(blank=True, default=None, null=True, verbose_name='url')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.page', verbose_name='page')),
            ],
            options={
                'verbose_name': 'redirect',
                'verbose_name_plural': 'redirects',
            },
        ),
        migrations.CreateModel(
            name='PageDraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_type', models.CharField(max_length=255, verbose_name='page type')),
                ('last_edited_at', models.DateField(auto_now=True, verbose_name='last edited at')),
                ('content_en', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_draft_en', to='website.contentobjectbase', verbose_name='english content')),
                ('content_sv', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_draft_sv', to='website.contentobjectbase', verbose_name='swedish content')),
                ('page', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_draft', to='website.page', verbose_name='page')),
            ],
            options={
                'verbose_name': 'page draft',
                'verbose_name_plural': 'page drafts',
            },
        ),
        migrations.CreateModel(
            name='NewsDraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_type', models.CharField(max_length=255, verbose_name='page type')),
                ('last_edited_at', models.DateField(auto_now=True, verbose_name='last edited at')),
                ('content_en', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news_draft_en', to='website.contentobjectbase', verbose_name='english content')),
                ('content_sv', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news_draft_sv', to='website.contentobjectbase', verbose_name='swedish content')),
                ('new', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news_draft', to='website.news', verbose_name='news')),
            ],
            options={
                'verbose_name': 'news draft',
                'verbose_name_plural': 'news drafts',
            },
        ),
        migrations.AddField(
            model_name='menuitembase',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='website.menu', verbose_name='menu'),
        ),
        migrations.AddField(
            model_name='menuitembase',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.page', verbose_name='page'),
        ),
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('contentobjectbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.contentobjectbase')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content_objects', to='website.page', verbose_name='page')),
            ],
            options={
                'verbose_name': 'page content object',
                'verbose_name_plural': 'page content objects',
            },
            bases=('website.contentobjectbase',),
        ),
        migrations.AddField(
            model_name='contentobjectbase',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='website.contentcollection', verbose_name='collection'),
        ),
        migrations.CreateModel(
            name='ContentMenu',
            fields=[
                ('contentobjectbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.contentobjectbase')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content_objects', to='website.menu', verbose_name='menu')),
            ],
            options={
                'verbose_name': 'menu content object',
                'verbose_name_plural': 'menu content objects',
            },
            bases=('website.contentobjectbase',),
        ),
        migrations.CreateModel(
            name='ContentImage',
            fields=[
                ('contentobjectbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.contentobjectbase')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content_objects', to='website.image', verbose_name='image')),
            ],
            options={
                'verbose_name': 'image content object',
                'verbose_name_plural': 'image content objects',
            },
            bases=('website.contentobjectbase',),
        ),
        migrations.AlterUniqueTogether(
            name='menuitembase',
            unique_together={('menu', 'name')},
        ),
    ]
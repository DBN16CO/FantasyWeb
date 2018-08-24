# Generated by Django 2.1 on 2018-08-24 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Draft_Pick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pick_time', models.DateTimeField(auto_now_add=True)),
                ('pick_round', models.IntegerField()),
                ('pick_position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('invite_id', models.CharField(max_length=100, null=True, unique=True)),
                ('draft_complete', models.BooleanField(default=False)),
                ('year_created', models.IntegerField()),
                ('cur_draft_round', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='League_Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=25)),
                ('cap_hit', models.IntegerField(default=0)),
                ('is_commish', models.BooleanField(default=False)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.League')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='League_Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('value', models.CharField(max_length=25)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.League')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('team', models.CharField(max_length=3)),
                ('number', models.CharField(max_length=3)),
                ('position', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=5)),
                ('height', models.CharField(max_length=5)),
                ('weight', models.CharField(max_length=5)),
                ('dob', models.CharField(max_length=10)),
                ('experience', models.CharField(max_length=3)),
                ('college', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Player_Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('length', models.IntegerField(default=1)),
                ('bid_time', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.League_Member')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Player_Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('length', models.IntegerField(default=1)),
                ('acquired', models.CharField(max_length=25)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.League')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.League_Member')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Player_Nomination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomination_time', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.League_Member')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.Player')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('name', 'dob', 'college')},
        ),
        migrations.AddField(
            model_name='draft_pick',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.League'),
        ),
        migrations.AddField(
            model_name='draft_pick',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.League_Member'),
        ),
        migrations.AddField(
            model_name='draft_pick',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='player_nomination',
            unique_together={('owner', 'player', 'nomination_time')},
        ),
        migrations.AlterUniqueTogether(
            name='player_contract',
            unique_together={('league', 'player')},
        ),
        migrations.AlterUniqueTogether(
            name='player_bid',
            unique_together={('owner', 'player', 'bid_time')},
        ),
        migrations.AlterUniqueTogether(
            name='league_setting',
            unique_together={('league', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='league_member',
            unique_together={('league', 'member'), ('league', 'team_name')},
        ),
        migrations.AlterUniqueTogether(
            name='draft_pick',
            unique_together={('league', 'player'), ('league', 'pick_round', 'pick_position')},
        ),
    ]

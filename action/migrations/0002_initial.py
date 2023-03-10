# Generated by Django 4.1.5 on 2023-01-10 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('action', '0001_initial'),
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatment',
            name='consultant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultant', to='manager.employee'),
        ),
        migrations.AddField(
            model_name='treatment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.customer'),
        ),
        migrations.AddField(
            model_name='treatment',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='manager.employee'),
        ),
        migrations.AddField(
            model_name='treatment',
            name='expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expert', to='manager.employee'),
        ),
        migrations.AddField(
            model_name='treatment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.service'),
        ),
        migrations.AddField(
            model_name='consulting',
            name='consultor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultor', to='manager.employee'),
        ),
        migrations.AddField(
            model_name='consulting',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.customer'),
        ),
    ]

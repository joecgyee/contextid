from django.db import models

class Context(models.Model):
    class Types(models.TextChoices):
        LEGAL = 'LEGAL', 'Legal'
        PROFESSIONAL = 'PROFESSIONAL', 'Professional'
        SOCIAL = 'SOCIAL', 'Social'
        CULTURAL = 'CULTURAL', 'Cultural'
        ONLINE = 'ONLINE', 'Online'
        POLITICAL = 'POLITICAL', 'Political'
        RELIGIOUS = 'RELIGIOUS', 'Religious/Spiritual'
        ECONOMIC = 'ECONOMIC', 'Economic'
        EDUCATIONAL = 'EDUCATIONAL', 'Educational/Academic'
        FAMILIAL = 'FAMILIAL', 'Familial'
        GENDER = 'GENDER', 'Gender'
        ETHNIC = 'ETHNIC', 'Ethnic/Racial'
        NATIONAL = 'NATIONAL', 'National/Regional'
        HEALTH = 'HEALTH', 'Health/Disability'
        DIGITAL = 'DIGITAL', 'Digital/Technological'

    name = models.CharField(
        max_length=50,
        choices=Types.choices,
        unique=True,
        default=Types.LEGAL
    )

    def __str__(self):
        return self.get_name_display()
            

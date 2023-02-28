from django.db import models
from PIL import Image
from django.urls import reverse


########################################################################################################################
class Work(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=50)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}({self.unit})'

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])


class Employee(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]

    name = models.CharField(max_length=50)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    telephoneNo = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    img = models.ImageField(upload_to='emp_images', default='default_emp.png')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.img.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.img.path)

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])


class Section(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to='section_images', default='default_section.png')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.img.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.img.path)

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])


class Entry(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True)

    amount = models.FloatField(default=0)
    description = models.TextField(blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.date)[0: 10] + ' by ' + self.employee.name

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])


# expectations for a month
class Employee_Work(models.Model):
    _employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    _work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True)
    value = models.FloatField(help_text='for 30 days')

    def __str__(self):
        return self._employee.name + '_' + self._work.name

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])


class Section_Work(models.Model):
    _section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    _work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True)
    value = models.FloatField(help_text='for 30 days')

    def __str__(self):
        return self._section.name + '_' + self._work.name

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])

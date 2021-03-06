# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from courses.models import Course


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True, validators=[
        RegexValidator(
            regex="^[\w]+[\w.%+-]*@iiu\.edu\.pk$",
            message='Please enter a valid IIUI email address'
        ),
    ], help_text='Enter your IIUI email address')
    profile_completion = models.BooleanField(default=False)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text=('Designates whether the user can log into this admin '
                                                             'site.'))
    is_active = models.BooleanField(default=True, help_text=('Designates whether this user should be treated as '
                                                             'active. Unselect this instead of deleting accounts.'))
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin
    #
    # def has_module_perms(self, add_label):
    #     return True


class Faculty(models.Model):
    faculty_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.faculty_name


class Department(models.Model):
    department_name = models.CharField(max_length=30)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.department_name


class Programme(models.Model):
    degree_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.degree_name


class Batch(models.Model):
    batch_name = models.CharField(max_length=14)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Batches"

    def __str__(self):
        return self.batch_name


class Section(models.Model):
    section_name = models.CharField(max_length=14)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return self.section_name


class StudentProfile(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 1.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    student = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='student_account')
    phone_number = models.CharField(max_length=20, help_text='Please use the format: "+923456789121"', validators=[
        RegexValidator(
            regex='^((\+92))(3)([0-9]{9})$',
            message='Please enter a valid Pakistan phone number'
        ),
    ])
    registration_number = models.CharField(max_length=6, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    fatherName = models.CharField(max_length=50, null=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=20,)
    cnic = models.CharField(max_length=30,)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True,
                                        validators=[validate_image])
    profile_picture_thumbnail = ImageSpecField(source='profile_picture',
                                               processors=[ResizeToFill(100, 100)],
                                               format='JPEG',
                                               options={'quality': 60})

    class Meta:
        verbose_name_plural = "Student Profiles"

    def __str__(self):
        return f"{self.registration_number} {self.student.first_name} {self.student.last_name} {self.batch.batch_name}"

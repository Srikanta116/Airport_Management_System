from django.db import models,transaction
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
import uuid
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        try:
            with transaction.atomic():
                user = self.model(username=username, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password=password, **extra_fields)


class User(AbstractBaseUser):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    last_name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    dob = models.DateField(null=True, blank=True)
    contact = models.BigIntegerField(default=0, db_index=True)
    username = models.CharField(max_length=100, blank=True, null=True, unique=True, db_index=True)


    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()


    last_attempt = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    by_bulk = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    
    employee_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    adhar_no = models.CharField(max_length=255, unique=True)
    salary = models.FloatField(blank=True, null=True)


    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['-date_joined']


class Role(models.Model):

    SUPERADMIN = 1
    ADMIN = 2
    AIRLINE_STAFF = 3
    AIRPORT_STAFF = 4
    SECURITY_STAFF = 5
    PASSENGER = 6

    ROLE_CHOICES = (
        (SUPERADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (AIRLINE_STAFF, 'Airline Staff'),
        (AIRPORT_STAFF, 'Airport Staff'),
        (SECURITY_STAFF, 'Security Staff'),
        (PASSENGER, 'Passenger')
    )

    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True)
    name = models.CharField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Airport(models.Model):
    airport_name=models.CharField(max_length=255)
    city=models.CharField(max_length=255,blank=True,null=True)
    area=models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Aeroplane(models.Model):
    aeroplane_id=models.CharField(max_length=255,unique=True)
    aeroplane_name=models.CharField(max_length=255)
    capacity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.aeroplane_name

class UserRoleMapping(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='air_group_user')
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    airport=models.ForeignKey(Airport,on_delete=models.DO_NOTHING,blank=True,null=True)
    airline=models.ForeignKey(Aeroplane,on_delete=models.DO_NOTHING,blank=True,null=True)
    
    def __str__(self):
        return self.user.username, self.role.name
    
class Runway(models.Model):
    airport=models.ForeignKey(Airport,on_delete=models.DO_NOTHING)
    runway_number=models.IntegerField()
    is_occupied=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.flight.flight_name, self.airport.airport_name

#

class Flight(models.Model):
    flight_id=models.CharField(max_length=255,unique=True)
    aeroplane = models.ForeignKey(Aeroplane,on_delete=models.DO_NOTHING)
    runway = models.ForeignKey(Runway,on_delete=models.DO_NOTHING)
    starting_time = models.DateTimeField()
    reach_time = models.DateTimeField()
    source = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name='source_airport')
    destination = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name='destination_airport')
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.flight_name

class TicketCounter(models.Model):
    ticket_id=models.CharField(max_length=255,unique=True)
    passenger=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    flight=models.ForeignKey(Flight,on_delete=models.DO_NOTHING)
    seat_no=models.IntegerField(null=True,blank=True)
    source=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name='source_tckt')
    destination=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name='destination_tckt')
    is_booked=models.BooleanField(default=False)
    is_checked=models.BooleanField(default=False)
    is_security_checked=models.BooleanField(default=False)
    is_boarded=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_id, self.passenger

class LuggageCounter(models.Model):
    luggage_id=models.CharField(max_length=255,unique=True)
    flight=models.ForeignKey(Flight,on_delete=models.DO_NOTHING)
    ticket=models.ForeignKey(TicketCounter,on_delete=models.DO_NOTHING)
    weight=models.FloatField(null=True,blank=True)
    no_of_luggage=models.IntegerField(null=True,blank=True)
    is_checked=models.BooleanField(default=False)
    is_boarded=models.BooleanField(default=False)
    is_security_checked=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.luggage_id, self.passenger

class NoticeBoard(models.Model):
    flight=models.ForeignKey(Flight,on_delete=models.DO_NOTHING)
    arraival_time=models.DateTimeField(default=None,blank=True,null=True)
    departure_time=models.DateTimeField(default=None,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.flight.flight_name, self.source, self.Destination






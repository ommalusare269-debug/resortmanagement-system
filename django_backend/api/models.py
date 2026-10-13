# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Attendance(models.Model):
    AttendanceID = models.AutoField(db_column='AttendanceID', primary_key=True)  # Field name made lowercase.
    StaffID = models.ForeignKey('Staff', models.DO_NOTHING, db_column='StaffID')  # Field name made lowercase.
    Date = models.DateField(db_column='Date')  # Field name made lowercase.
    Status = models.CharField(db_column='Status', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'attendance'
        unique_together = (('StaffID', 'Date'),)


class BookingServices(models.Model):
    BookingServiceID = models.AutoField(db_column='BookingServiceID', primary_key=True)  # Field name made lowercase.
    BookingID = models.ForeignKey('Bookings', models.DO_NOTHING, db_column='BookingID')  # Field name made lowercase.
    ServiceID = models.ForeignKey('Services', models.DO_NOTHING, db_column='ServiceID')  # Field name made lowercase.
    Qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.
    Amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    Status = models.CharField(db_column='Status', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'booking_services'


class Bookings(models.Model):
    BookingID = models.AutoField(db_column='BookingID', primary_key=True)  # Field name made lowercase.
    CustomerID = models.ForeignKey('Customers', models.DO_NOTHING, db_column='CustomerID')  # Field name made lowercase.
    CheckInDate = models.DateField(db_column='CheckInDate')  # Field name made lowercase.
    CheckOutDate = models.DateField(db_column='CheckOutDate')  # Field name made lowercase.
    NoOfGuests = models.IntegerField(db_column='NoOfGuests')  # Field name made lowercase.
    BookingDate = models.DateTimeField(db_column='BookingDate', blank=True, null=True)  # Field name made lowercase.
    Status = models.CharField(db_column='Status', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bookings'


class Customers(models.Model):
    CustomerID = models.AutoField(db_column='CustomerID', primary_key=True)  # Field name made lowercase.
    Name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    Phone = models.CharField(db_column='Phone', max_length=15)  # Field name made lowercase.
    Email = models.CharField(db_column='Email', unique=True, max_length=100)  # Field name made lowercase.
    Address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    PasswordHash = models.CharField(db_column='PasswordHash', max_length=255)  # Field name made lowercase.
    CreatedAt = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customers'


class Invoices(models.Model):
    InvoiceID = models.AutoField(db_column='InvoiceID', primary_key=True)  # Field name made lowercase.
    BookingID = models.ForeignKey(Bookings, models.DO_NOTHING, db_column='BookingID')  # Field name made lowercase.
    InvoiceDate = models.DateField(db_column='InvoiceDate')  # Field name made lowercase.
    TotalAmount = models.DecimalField(db_column='TotalAmount', max_digits=12, decimal_places=2)  # Field name made lowercase.
    Discount = models.DecimalField(db_column='Discount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    GrandTotal = models.DecimalField(db_column='GrandTotal', max_digits=12, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoices'


class Payments(models.Model):
    PaymentID = models.AutoField(db_column='PaymentID', primary_key=True)  # Field name made lowercase.
    InvoiceID = models.ForeignKey(Invoices, models.DO_NOTHING, db_column='InvoiceID')  # Field name made lowercase.
    PaymentDate = models.DateField(db_column='PaymentDate')  # Field name made lowercase.
    Amount = models.DecimalField(db_column='Amount', max_digits=12, decimal_places=2)  # Field name made lowercase.
    PaymentMode = models.CharField(db_column='PaymentMode', max_length=50)  # Field name made lowercase.
    TxnReference = models.CharField(db_column='TxnReference', max_length=100, blank=True, null=True)  # Field name made lowercase.
    Status = models.CharField(db_column='Status', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payments'


class RoomAllocations(models.Model):
    AllocationID = models.AutoField(db_column='AllocationID', primary_key=True)  # Field name made lowercase.
    BookingID = models.ForeignKey(Bookings, models.DO_NOTHING, db_column='BookingID')  # Field name made lowercase.
    RoomID = models.ForeignKey('Rooms', models.DO_NOTHING, db_column='RoomID')  # Field name made lowercase.
    CheckInDate = models.DateField(db_column='CheckInDate')  # Field name made lowercase.
    CheckOutDate = models.DateField(db_column='CheckOutDate')  # Field name made lowercase.
    Rate = models.DecimalField(db_column='Rate', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'room_allocations'


class RoomTypes(models.Model):
    RoomTypeID = models.AutoField(db_column='RoomTypeID', primary_key=True)  # Field name made lowercase.
    TypeName = models.CharField(db_column='TypeName', max_length=50)  # Field name made lowercase.
    Description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Capacity = models.IntegerField(db_column='Capacity')  # Field name made lowercase.
    Rate = models.DecimalField(db_column='Rate', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'room_types'


class Rooms(models.Model):
    RoomID = models.AutoField(db_column='RoomID', primary_key=True)  # Field name made lowercase.
    RoomTypeID = models.ForeignKey(RoomTypes, models.DO_NOTHING, db_column='RoomTypeID')  # Field name made lowercase.
    RoomNo = models.CharField(db_column='RoomNo', unique=True, max_length=10)  # Field name made lowercase.
    FloorNo = models.IntegerField(db_column='FloorNo', blank=True, null=True)  # Field name made lowercase.
    Status = models.CharField(db_column='Status', max_length=20)  # Field name made lowercase.
    CleaningStatus = models.CharField(db_column='CleaningStatus', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rooms'


class Services(models.Model):
    ServiceID = models.AutoField(db_column='ServiceID', primary_key=True)  # Field name made lowercase.
    ServiceName = models.CharField(db_column='ServiceName', max_length=100)  # Field name made lowercase.
    Description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Charge = models.DecimalField(db_column='Charge', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'services'


class Settings(models.Model):
    Key = models.CharField(db_column='Key', primary_key=True, max_length=100)  # Field name made lowercase.
    Value = models.TextField(db_column='Value')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'settings'


class Staff(models.Model):
    StaffID = models.AutoField(db_column='StaffID', primary_key=True)  # Field name made lowercase.
    Name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    Role = models.CharField(db_column='Role', max_length=50)  # Field name made lowercase.
    Phone = models.CharField(db_column='Phone', max_length=15)  # Field name made lowercase.
    Email = models.CharField(db_column='Email', unique=True, max_length=100)  # Field name made lowercase.
    PasswordHash = models.CharField(db_column='PasswordHash', max_length=255)  # Field name made lowercase.
    Salary = models.DecimalField(db_column='Salary', max_digits=10, decimal_places=2)  # Field name made lowercase.
    Department = models.CharField(db_column='Department', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'staff'

class Inquiries(models.Model):
    InquiryID = models.AutoField(primary_key=True)
    CustomerName = models.CharField(max_length=255)
    CustomerEmail = models.EmailField()
    Phone = models.CharField(max_length=20, null=True, blank=True)
    CheckInDate = models.DateField(null=True, blank=True)
    CheckOutDate = models.DateField(null=True, blank=True)
    Guests = models.IntegerField(null=True, blank=True)
    RoomType = models.CharField(max_length=100, null=True, blank=True)
    InquiryType = models.CharField(max_length=100, null=True, blank=True)
    Subject = models.CharField(max_length=255, null=True, blank=True)
    Message = models.TextField()
    Status = models.CharField(max_length=50, default='PENDING')
    CreatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'inquiries'


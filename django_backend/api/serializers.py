from rest_framework import serializers
from .models import (
    Customers, RoomTypes, Rooms, Bookings, RoomAllocations,
    Services, BookingServices, Staff, Attendance, Invoices, Payments, Settings, Inquiries
)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTypes
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    RoomType = RoomTypeSerializer(source='RoomTypeID', read_only=True)
    class Meta:
        model = Rooms
        fields = '__all__'

class RoomAllocationSerializer(serializers.ModelSerializer):
    Room = RoomSerializer(source='RoomID', read_only=True)
    class Meta:
        model = RoomAllocations
        fields = '__all__'

class BookingServiceSerializer(serializers.ModelSerializer):
    # Service details will be nested in view or customized if needed
    class Meta:
        model = BookingServices
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    Payments = PaymentSerializer(source='payments_set', many=True, read_only=True)
    class Meta:
        model = Invoices
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    Customer = CustomerSerializer(source='CustomerID', read_only=True)
    RoomAllocations = RoomAllocationSerializer(source='roomallocations_set', many=True, read_only=True)
    Invoices = InvoiceSerializer(source='invoices_set', many=True, read_only=True)
    BookingServices = BookingServiceSerializer(source='bookingservices_set', many=True, read_only=True)
    
    class Meta:
        model = Bookings
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiries
        fields = '__all__'


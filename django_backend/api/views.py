from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import *
from .serializers import *
import jwt
import bcrypt
from datetime import datetime, timedelta

JWT_SECRET = "resort_super_secret_key_2026_for_dev_only"

@api_view(['POST'])
def auth_login(request):
    email = request.data.get('Email', request.data.get('email'))
    password = request.data.get('Password', request.data.get('password'))

    # First check Customers
    try:
        user = Customers.objects.get(Email=email)
        if bcrypt.checkpw(password.encode('utf-8'), user.PasswordHash.encode('utf-8')) or user.PasswordHash == password:
            token = jwt.encode({'id': user.CustomerID, 'role': 'CUSTOMER'}, JWT_SECRET, algorithm='HS256')
            return Response({'token': token, 'user': {'id': user.CustomerID, 'name': user.Name, 'email': user.Email, 'role': 'CUSTOMER'}})
    except Customers.DoesNotExist:
        pass

    # Then check Staff
    try:
        staff_user = Staff.objects.get(Email=email)
        if bcrypt.checkpw(password.encode('utf-8'), staff_user.PasswordHash.encode('utf-8')) or staff_user.PasswordHash == password:
            token = jwt.encode({'id': staff_user.StaffID, 'role': staff_user.Role}, JWT_SECRET, algorithm='HS256')
            return Response({'token': token, 'user': {'id': staff_user.StaffID, 'name': staff_user.Name, 'email': staff_user.Email, 'role': staff_user.Role}})
    except Staff.DoesNotExist:
        pass

    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
def auth_register(request):
    data = request.data
    password = data.get('Password', '')
    email = data.get('Email', '')
    
    if Customers.objects.filter(Email=email).exists():
        return Response({'error': 'Email address is already in use.'}, status=400)
        
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        user = Customers.objects.create(
            Name=data.get('Name'),
            Phone=data.get('Phone'),
            Email=email,
            PasswordHash=hashed,
            Address=data.get('Address', 'N/A'),
            CreatedAt=datetime.now()
        )
        token = jwt.encode({'id': user.CustomerID, 'role': 'CUSTOMER'}, JWT_SECRET, algorithm='HS256')
        return Response({'token': token, 'user': {'id': user.CustomerID, 'name': user.Name, 'email': user.Email, 'role': 'CUSTOMER'}})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def auth_me(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response({'error': 'No token provided'}, status=401)
    token = auth_header.split(' ')[1]
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        if decoded['role'] == 'CUSTOMER':
            user = Customers.objects.get(pk=decoded['id'])
            return Response({'user': {'id': user.CustomerID, 'name': user.Name, 'email': user.Email, 'role': 'CUSTOMER'}})
        else:
            user = Staff.objects.get(pk=decoded['id'])
            return Response({'user': {'id': user.StaffID, 'name': user.Name, 'email': user.Email, 'role': user.Role}})
    except:
        return Response({'error': 'Invalid token'}, status=401)

@api_view(['POST'])
def change_password(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response({'error': 'No token provided'}, status=401)
    try:
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        new_password = request.data.get('new_password')
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        if decoded['role'] == 'CUSTOMER':
            user = Customers.objects.get(pk=decoded['id'])
            user.PasswordHash = hashed
            user.save()
        else:
            user = Staff.objects.get(pk=decoded['id'])
            user.PasswordHash = hashed
            user.save()
        return Response({'message': 'Password changed successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Cascade delete manually since DB has RESTRICT
        bookings = Bookings.objects.filter(CustomerID=instance.CustomerID)
        for booking in bookings:
            BookingServices.objects.filter(BookingID=booking.BookingID).delete()
            RoomAllocations.objects.filter(BookingID=booking.BookingID).delete()
            invoices = Invoices.objects.filter(BookingID=booking.BookingID)
            for inv in invoices:
                Payments.objects.filter(InvoiceID=inv.InvoiceID).delete()
            invoices.delete()
        bookings.delete()
        self.perform_destroy(instance)
        return Response(status=204)

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomTypes.objects.all()
    serializer_class = RoomTypeSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_rooms = Rooms.objects.filter(Status__iexact='AVAILABLE')
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def status(self, request, pk=None):
        room = self.get_object()
        room.Status = request.data.get('Status', room.Status)
        room.save()
        return Response(self.get_serializer(room).data)

    @action(detail=True, methods=['put'])
    def cleaning(self, request, pk=None):
        room = self.get_object()
        room.CleaningStatus = request.data.get('CleaningStatus', room.CleaningStatus)
        room.save()
        return Response(self.get_serializer(room).data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all().order_by('-BookingDate')
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        customer_id = data.get('CustomerID')
        room_id = data.get('RoomID')
        check_in = data.get('CheckInDate')
        check_out = data.get('CheckOutDate')
        guests = data.get('NoOfGuests')

        if not all([customer_id, check_in, check_out, guests, room_id]):
            return Response({'error': 'Missing required booking fields'}, status=400)

        overlapping = RoomAllocations.objects.filter(
            RoomID=room_id,
            CheckInDate__lt=check_out,
            CheckOutDate__gt=check_in
        ).exclude(BookingID__Status__in=['CANCELLED', 'CHECKED_OUT'])
        if overlapping.exists():
            return Response({'error': 'Room is not available for selected dates'}, status=409)

        try:
            room = Rooms.objects.get(pk=room_id)
            customer = Customers.objects.get(pk=customer_id)
        except:
            return Response({'error': 'Room or Customer not found'}, status=404)

        booking = Bookings.objects.create(
            CustomerID=customer,
            CheckInDate=check_in,
            CheckOutDate=check_out,
            NoOfGuests=guests,
            Status='CONFIRMED',
            BookingDate=datetime.now()
        )
        
        RoomAllocations.objects.create(
            BookingID=booking,
            RoomID=room,
            CheckInDate=check_in,
            CheckOutDate=check_out,
            Rate=room.RoomTypeID.Rate
        )
        
        return Response({
            'message': 'Booking created successfully',
            'booking': BookingSerializer(booking).data
        }, status=201)

    @action(detail=True, methods=['put'])
    def status(self, request, pk=None):
        booking = self.get_object()
        new_status = request.data.get('Status', booking.Status)
        
        if new_status == 'CHECKED_OUT' and booking.Status != 'CHECKED_OUT':
            # Check if invoice already exists
            if not Invoices.objects.filter(BookingID=booking).exists():
                room_charges = 0
                for alloc in booking.roomallocations_set.all():
                    end_date = alloc.CheckOutDate.date() if hasattr(alloc.CheckOutDate, 'date') else alloc.CheckOutDate
                    start_date = alloc.CheckInDate.date() if hasattr(alloc.CheckInDate, 'date') else alloc.CheckInDate
                    days = (end_date - start_date).days
                    if days <= 0: days = 1
                    room_charges += days * alloc.Rate
                
                service_charges = sum(svc.Amount for svc in booking.bookingservices_set.all())
                
                total = room_charges + service_charges
                from django.utils import timezone
                Invoices.objects.create(
                    BookingID=booking,
                    InvoiceDate=timezone.now(),
                    TotalAmount=total,
                    Discount=0,
                    GrandTotal=total
                )

        booking.Status = new_status
        booking.save()
        return Response(self.get_serializer(booking).data)

    @action(detail=False, methods=['get'], url_path=r'customer/(?P<customer_id>[^/.]+)')
    def customer_bookings(self, request, customer_id=None):
        bookings = Bookings.objects.filter(CustomerID=customer_id).order_by('-BookingDate')
        return Response(BookingSerializer(bookings, many=True).data)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer

    @action(detail=False, methods=['post'], url_path='add-to-booking')
    def add_to_booking(self, request):
        b_id = request.data.get('BookingID')
        s_id = request.data.get('ServiceID')
        qty = request.data.get('Qty', 1)
        try:
            service = Services.objects.get(pk=s_id)
            booking = Bookings.objects.get(pk=b_id)
            BookingServices.objects.create(
                BookingID=booking,
                ServiceID=service,
                Qty=qty,
                Amount=service.Charge * int(qty),
                Status='Pending'
            )
            return Response({'message': 'Service added'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['get'], url_path='tasks')
    def tasks(self, request):
        tasks = BookingServices.objects.all().order_by('-BookingServiceID')
        return Response(BookingServiceSerializer(tasks, many=True).data)

    @action(detail=False, methods=['put'], url_path=r'tasks/(?P<task_id>[^/.]+)/status')
    def task_status(self, request, task_id=None):
        try:
            task = BookingServices.objects.get(pk=task_id)
            task.Status = request.data.get('Status', task.Status)
            task.save()
            return Response({'message': 'Task updated'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'Password' in data:
            data['PasswordHash'] = bcrypt.hashpw(data.pop('Password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['put'])
    def department(self, request, pk=None):
        staff = self.get_object()
        staff.Department = request.data.get('Department', staff.Department)
        staff.save()
        return Response(self.get_serializer(staff).data)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoices.objects.all()
    serializer_class = InvoiceSerializer

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingSerializer

@api_view(['GET', 'POST'])
def settings_list(request):
    if request.method == 'GET':
        settings = Settings.objects.all()
        data = {s.Key: s.Value for s in settings}
        return Response(data)
    elif request.method == 'POST':
        for key, value in request.data.items():
            Settings.objects.update_or_create(Key=key, defaults={'Value': value})
        return Response({'message': 'Settings updated'})

@api_view(['GET'])
def get_dashboard_stats(request):
    from django.db.models import Sum
    from datetime import datetime, timedelta
    import calendar

    # Totals
    total_revenue = Payments.objects.filter(Status='SUCCESS').aggregate(total=Sum('Amount'))['total'] or 0
    total_customers = Customers.objects.count()
    total_rooms = Rooms.objects.count()
    active_bookings = Bookings.objects.filter(Status='CHECKED_IN').count()

    timeframe = request.query_params.get('timeframe', 'monthly')
    chart_data = []
    today = datetime.today()

    if timeframe == 'daily':
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            start_date = datetime(date.year, date.month, date.day, 0, 0, 0)
            end_date = datetime(date.year, date.month, date.day, 23, 59, 59)
            revenue = Payments.objects.filter(Status='SUCCESS', PaymentDate__gte=start_date, PaymentDate__lte=end_date).aggregate(total=Sum('Amount'))['total'] or 0
            chart_data.append({'name': date.strftime('%a'), 'revenue': float(revenue)})
            
    elif timeframe == 'weekly':
        for i in range(6, -1, -1):
            date = today - timedelta(weeks=i)
            start_date = date - timedelta(days=date.weekday())
            end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
            revenue = Payments.objects.filter(Status='SUCCESS', PaymentDate__gte=start_date, PaymentDate__lte=end_date).aggregate(total=Sum('Amount'))['total'] or 0
            chart_data.append({'name': f'W{start_date.isocalendar()[1]}', 'revenue': float(revenue)})

    elif timeframe == 'yearly':
        for i in range(4, -1, -1):
            year = today.year - i
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31, 23, 59, 59)
            revenue = Payments.objects.filter(Status='SUCCESS', PaymentDate__gte=start_date, PaymentDate__lte=end_date).aggregate(total=Sum('Amount'))['total'] or 0
            chart_data.append({'name': str(year), 'revenue': float(revenue)})

    else: # monthly (default)
        for i in range(6, -1, -1):
            month = today.month - i
            year = today.year
            if month <= 0:
                month += 12
                year -= 1
            start_date = datetime(year, month, 1)
            _, last_day = calendar.monthrange(year, month)
            end_date = datetime(year, month, last_day, 23, 59, 59)
            revenue = Payments.objects.filter(Status='SUCCESS', PaymentDate__gte=start_date, PaymentDate__lte=end_date).aggregate(total=Sum('Amount'))['total'] or 0
            chart_data.append({'name': calendar.month_abbr[month], 'revenue': float(revenue)})

    return Response({
        'totalCustomers': total_customers,
        'totalRooms': total_rooms,
        'activeBookings': active_bookings,
        'totalRevenue': float(total_revenue),
        'chartData': chart_data
    })

@api_view(['GET'])
def attendance_by_date(request, date_str):
    date_obj = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d').date()
    att = Attendance.objects.filter(Date=date_obj)
    return Response(AttendanceSerializer(att, many=True).data)

@api_view(['POST'])
def mark_attendance(request):
    date_str = request.data.get('Date')
    date_obj = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d').date()
    for record in request.data.get('Records', []):
        try:
            staff = Staff.objects.get(pk=record['StaffID'])
            Attendance.objects.update_or_create(
                StaffID=staff,
                Date=date_obj,
                defaults={'Status': record['Status']}
            )
        except Exception:
            pass
    return Response({'message': 'Attendance marked'})

@api_view(['POST'])
def add_payment(request):
    inv_id = request.data.get('InvoiceID')
    amt = request.data.get('Amount')
    mode = request.data.get('PaymentMode', 'Cash')
    try:
        inv = Invoices.objects.get(pk=inv_id)
        Payments.objects.create(
            InvoiceID=inv,
            PaymentDate=datetime.now(),
            Amount=amt,
            PaymentMode=mode,
            Status='SUCCESS',
            TxnReference='TXN' + str(int(datetime.now().timestamp()))
        )
        return Response({'message': 'Payment added'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiries.objects.all().order_by('-CreatedAt')
    serializer_class = InquirySerializer


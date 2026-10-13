from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter(trailing_slash=False)
router.register(r'customers', CustomerViewSet)
router.register(r'rooms/types', RoomTypeViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'billing/invoices', InvoiceViewSet)
router.register(r'inquiries', InquiryViewSet)

urlpatterns = [
    path('auth/login', auth_login),
    path('auth/register', auth_register),
    path('auth/me', auth_me),
    path('auth/change-password', change_password),
    path('settings', settings_list),
    path('reports/stats', get_dashboard_stats),
    path('attendance/date/<str:date_str>', attendance_by_date),
    path('attendance/mark', mark_attendance),
    path('billing/payment', add_payment),
    path('', include(router.urls)),
]

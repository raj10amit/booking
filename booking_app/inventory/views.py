from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Member, Inventory, Booking
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt



MAX_BOOKINGS = 2
@csrf_exempt
@require_http_methods(["POST"])
def book_item(request):
    member_id = request.POST.get('member_id')
    item_id = request.POST.get('item_id')

    if not member_id or not item_id:
        return JsonResponse({'status': 'error', 'message': 'Missing parameters!'})

    try:
        member = Member.objects.get(id=member_id)
        item = Inventory.objects.get(id=item_id)

        if item.remaining_count <= 0:
            return JsonResponse({'status': 'error', 'message': 'Item not available!'})

        # Create a new booking entry
        booking = Booking.objects.create(
            member=member,
            inventory=item,
            booking_date=timezone.now()
        )

        # Update counts
        member.booking_count += 1
        member.save()
        item.remaining_count -= 1
        item.save()

        return JsonResponse({'status': 'success', 'message': 'Item booked successfully!', 'booking_id': booking.id})

    except Member.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Member not found!'})
    except Inventory.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@require_http_methods(["GET"])
def cancel_booking(request):
    booking_id = request.GET.get('booking_id')

    if not booking_id:
        return JsonResponse({'error': 'Missing booking_id'}, status=400)

    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)

    member = booking.member
    item = booking.inventory

    # Prevent negative counts
    if member.booking_count <= 0 or item.remaining_count < 0:
        return JsonResponse({'error': 'Invalid booking or item count'}, status=400)

    # Perform cancellation
    booking.delete()
    member.booking_count = max(0, member.booking_count - 1)
    member.save()
    item.remaining_count += 1
    item.save()

    return JsonResponse({'message': 'Booking cancelled successfully!'}, status=200)
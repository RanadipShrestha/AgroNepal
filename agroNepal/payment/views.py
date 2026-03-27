from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from esewa.signature import generate_signature
from agro.models import Event
from .models import PurchaseTicket
from user.models import CustomUser
import uuid
import hmac
import hashlib
import base64
import json
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Verify the data coming from eSewa
def verify_signature_from_esewa(payment_data):
    try:
        received_signature = payment_data.get('signature')
        if not received_signature:
            return False
            
        signed_field_names = payment_data.get('signed_field_names')
        if not signed_field_names:
            return False
        
        fields = signed_field_names.split(',')
        message_parts = []
        
        for field in fields:
            value = payment_data.get(field)
            message_parts.append(f"{field}={value}")
        
        message = ",".join(message_parts)
        secret_key = "8gBm/:&EnhH.1/q"
        
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        expected_signature_base64 = base64.b64encode(expected_signature).decode('utf-8')
        return received_signature == expected_signature_base64
        
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False

@login_required
def buy_ticket(request, slug):
    event = get_object_or_404(Event, slug=slug)
    user = request.user

    if event.available_ticket <= 0:
        return render(request, 'pages/event/payment_error.html', {
            'error_title': 'Sold Out',
            'error_message': 'Sorry, tickets for this event are sold out.',
            'show_retry': False
        })

    transaction_uuid = uuid.uuid4()
    signature = generate_signature(event.price, transaction_uuid)

    # ✅ Save to DB before redirecting to eSewa - this ensures we can find it even if sessions fail
    PurchaseTicket.objects.create(
        ticket_id=transaction_uuid,
        event=event,
        user=user,
        status=PurchaseTicket.STATUS_PENDING,
        amount=event.price
    )

    context = {
        'event': event,
        'transaction_uuid': transaction_uuid,
        'signature': signature,
    }
    return render(request, "pages/event/ticket_buy.html", context)

@login_required
def payment_success(request):
    encoded_data = request.GET.get('data')

    if not encoded_data:
        return render(request, 'pages/event/payment_error.html', {
            'error_title': 'Payment Data Missing',
            'error_message': "We didn't receive payment confirmation from eSewa.",
            'show_retry': True
        })

    try:
        decoded_bytes = base64.b64decode(encoded_data)
        payment_data = json.loads(decoded_bytes.decode('utf-8'))

        if not verify_signature_from_esewa(payment_data):
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Invalid Signature',
                'error_message': 'Payment verification failed.',
                'show_contact': True
            })

        status = payment_data.get('status')
        if status != "COMPLETE":
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Payment Incomplete',
                'error_message': f'Payment status is "{status}".',
                'show_retry': True
            })

        transaction_uuid = payment_data.get('transaction_uuid')
        ticket = get_object_or_404(PurchaseTicket, ticket_id=transaction_uuid)

        # Already completed - just show the ticket
        if ticket.status == PurchaseTicket.STATUS_COMPLETE:
            return render(request, "pages/event/ticket.html", {"ticket": ticket})

        # Verify amount - eSewa may include commas like "1,000.0"
        try:
            raw_amount = payment_data.get('total_amount', '0')
            clean_amount = str(raw_amount).replace(',', '')
            total_amount = Decimal(clean_amount)
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing amount '{raw_amount}': {e}")
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Data Error',
                'error_message': f"Invalid amount format from eSewa: {raw_amount}",
                'show_contact': True
            })

        if total_amount != ticket.amount:
            logger.warning(f"Amount mismatch for ticket {transaction_uuid}: expected {ticket.amount}, got {total_amount}")
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Amount Mismatch',
                'error_message': f"Expected Rs. {ticket.amount}, but received Rs. {total_amount}.",
                'show_contact': True
            })

        # Atomic update
        from django.db import transaction as db_transaction
        with db_transaction.atomic():
            # Refresh from DB with lock
            event = Event.objects.select_for_update().get(id=ticket.event.id)
            if event.available_ticket <= 0:
                return render(request, 'pages/event/payment_error.html', {
                    'error_title': 'Sold Out',
                    'error_message': 'Tickets sold out before your payment completed.',
                    'show_retry': False
                })
            
            ticket.status = PurchaseTicket.STATUS_COMPLETE
            ticket.save()
            event.book_ticket()

        return render(request, "pages/event/ticket.html", {"ticket": ticket})

    except Exception as e:
        import traceback
        logger.error(f"Exception in payment_success: {e}\n{traceback.format_exc()}")
        return render(request, 'pages/event/payment_failure.html', {
            'error_message': str(e),
            'transaction_uuid': request.GET.get('transaction_uuid') or (payment_data.get('transaction_uuid') if 'payment_data' in locals() else None)
        })

def payment_failure(request):
    return render(request, "pages/event/payment_failure.html")
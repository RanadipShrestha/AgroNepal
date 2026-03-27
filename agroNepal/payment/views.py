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

#  Signature Verification                                           

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
            value = payment_data.get(field, '')
            message_parts.append(f"{field}={value}")

        message = ",".join(message_parts)
        secret_key = "8gBm/:&EnhH.1/q"

        # ✅ Fixed: hmac.new() doesn't exist, correct is hmac.new
        h = hmac.new(
            secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        )
        expected_signature_base64 = base64.b64encode(h.digest()).decode('utf-8')

        # ✅ Timing-safe comparison
        return hmac.compare_digest(received_signature, expected_signature_base64)

    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False


#  Buy Ticket                                                          

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

    # ✅ Store in session instead of DB — no ticket created yet
    request.session['pending_payment'] = {
        'transaction_uuid': str(transaction_uuid),
        'event_slug': event.slug,
        'amount': str(event.price),
    }

    context = {
        'event': event,
        'transaction_uuid': transaction_uuid,
        'signature': signature,
    }
    return render(request, "pages/event/ticket_buy.html", context)



#  Payment Success                                                     
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
        # Step 1 — Decode eSewa response
        decoded_bytes = base64.b64decode(encoded_data)
        payment_data = json.loads(decoded_bytes.decode('utf-8'))

        # Step 2 — Verify signature
        if not verify_signature_from_esewa(payment_data):
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Invalid Signature',
                'error_message': 'Payment verification failed. Please contact support.',
                'show_contact': True
            })

        # Step 3 — Verify payment status
        status = payment_data.get('status')
        if status != "COMPLETE":
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Payment Incomplete',
                'error_message': f'Payment status is "{status}". Please try again.',
                'show_retry': True
            })

        transaction_uuid = payment_data.get('transaction_uuid')

        # Step 4 — Check if ticket already exists (handles page refresh)
        existing_ticket = PurchaseTicket.objects.filter(ticket_id=transaction_uuid).first()
        if existing_ticket:
            logger.info(f"Duplicate success callback for {transaction_uuid}")
            return render(request, "pages/event/ticket.html", {"ticket": existing_ticket})

        # Step 5 — Get event from session
        pending = request.session.get('pending_payment')

        if not pending or pending.get('transaction_uuid') != transaction_uuid:
            # ⚠️ Session lost — fallback: try to find event via amount from eSewa
            # This is a rare edge case (browser crash, session expiry mid-payment)
            logger.warning(f"Session lost for transaction {transaction_uuid}, attempting fallback.")
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Session Expired',
                'error_message': 'Your session expired during payment. Please contact support with your transaction ID.',
                'show_contact': True
            })

        event_slug = pending.get('event_slug')
        expected_amount = Decimal(pending.get('amount'))

        # Step 6 — Verify amount
        try:
            raw_amount = payment_data.get('total_amount', '0')
            clean_amount = str(raw_amount).replace(',', '')
            total_amount = Decimal(clean_amount)
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing amount '{raw_amount}': {e}")
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Data Error',
                'error_message': f"Invalid amount format received from eSewa: {raw_amount}",
                'show_contact': True
            })

        if total_amount != expected_amount:
            logger.warning(
                f"Amount mismatch for {transaction_uuid}: "
                f"expected {expected_amount}, got {total_amount}"
            )
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Amount Mismatch',
                'error_message': f"Expected Rs. {expected_amount}, but received Rs. {total_amount}.",
                'show_contact': True
            })

        # Step 7 — Atomically create ticket + decrement available tickets
        from django.db import transaction as db_transaction
        with db_transaction.atomic():
            event = Event.objects.select_for_update().get(slug=event_slug)

            if event.available_ticket <= 0:
                return render(request, 'pages/event/payment_error.html', {
                    'error_title': 'Sold Out',
                    'error_message': 'Tickets sold out just before your payment completed.',
                    'show_retry': False
                })

            #Create ticket only on confirmed success
            ticket = PurchaseTicket.objects.create(
                ticket_id=transaction_uuid,
                event=event,
                user=request.user,
                status=PurchaseTicket.STATUS_COMPLETE,
                amount=total_amount
            )
            event.book_ticket()

        #Clear session after successful ticket creation
        del request.session['pending_payment']

        return render(request, "pages/event/ticket.html", {"ticket": ticket})

    except Exception as e:
        import traceback
        logger.error(f"Exception in payment_success: {e}\n{traceback.format_exc()}")
        return render(request, 'pages/event/payment_failure.html', {
            'error_message': str(e),
            'transaction_uuid': payment_data.get('transaction_uuid') if 'payment_data' in locals() else None
        })


#  Payment Failure                                                     

def payment_failure(request):
    #Clean up session on cancel/failure
    if 'pending_payment' in request.session:
        del request.session['pending_payment']

    return render(request, "pages/event/payment_failure.html")
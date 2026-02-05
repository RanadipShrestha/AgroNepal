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

#Verify the data comming from the esewa. 
def verify_signature_from_esewa(payment_data):
    try:
        # Checking there is signature or not in the data
        received_signature = payment_data.get('signature')
        if not received_signature:
            return False
        # Getting the signed fields
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
            #Converting the secret_key into bytes 
            secret_key.encode('utf-8'),
            #Converting the message into bytes
            message.encode('utf-8'),
            #Hashing algorithm
            hashlib.sha256
        ).digest()
        
        expected_signature_base64 = base64.b64encode(expected_signature).decode('utf-8')
        #If the signatures is same then valid
        return received_signature == expected_signature_base64
        
    except Exception:
        return False


@login_required
def buy_ticket(request, id):
    event = get_object_or_404(Event, id=id)
    user = request.user
    
    if event.available_ticket <= 0:
        return render(request, 'pages/event/payment_error.html', {
            'error_title': 'Sold Out',
            'error_message': 'Sorry, tickets for this event are sold out.',
            'show_retry': False
        })
    
    transaction_uuid = uuid.uuid4()
    signature = generate_signature(event.price, transaction_uuid)
    
    session_key = f'payment_{transaction_uuid}'
    request.session[session_key] = {
        'event_id': event.id,
        'user_id': user.id,
        'amount': float(event.price),
    }
    context = {
        'event': event,
        'transaction_uuid': transaction_uuid,
        'signature': signature,
    }
    
    return render(request, "pages/event/ticket_buy.html", context)


def payment_success(request):
    #esewa la payment data send garxa Base64 encoded string ma in URL parameter data
    encoded_data = request.GET.get('data')
    
    # Check data xa ki nai
    if not encoded_data:
        #if data xaina vana paymenet_error page me render gardena with all those details
        return render(request, 'pages/event/payment_error.html', {
            'error_title': 'Payment Data Missing',
            'error_message': "We didn't receive payment confirmation from eSewa. Please try again or contact support.",
            'show_retry': True
        })
    
    try:
        ''' esewa la Base64(JSON) format ma data send garxa 
            We need to decode Base64 and get JSON string then parse to python dictionary 
        '''
        # First ma decode gara ko and get raw bytes
        decoded_bytes = base64.b64decode(encoded_data)
        # Second ma chai convert that bytes to string 
        decoded_str = decoded_bytes.decode('utf-8')
        # Thired ma chai parse that json string to python dictionary 
        payment_data = json.loads(decoded_str)
        
        if not verify_signature_from_esewa(payment_data):
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Invalid Signature',
                'error_message': 'Payment verification failed. This may be a fraudulent transaction.',
                'show_contact': True
            })
        
        status = payment_data.get('status')
        if status != "COMPLETE":
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Payment Incomplete',
                'error_message': f'Your payment status is "{status}". Please complete the payment or try again.',
                'show_retry': True
            })
        
        transaction_uuid = payment_data.get('transaction_uuid')
        total_amount = float(payment_data.get('total_amount'))
        #This will Prevent Duplicate tickets
        if PurchaseTicket.objects.filter(ticket_id=transaction_uuid).exists():
            ticket = PurchaseTicket.objects.get(ticket_id=transaction_uuid)
            return render(request, "pages/event/ticket.html", {
                'ticket': ticket,
                'message': "You already have this ticket!"
            })
        
        session_key = f'payment_{transaction_uuid}'
        payment_info = request.session.get(session_key)
        
        if not payment_info:
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Session Expired',
                'error_message': 'Your payment session has expired. Please start the purchase process again.',
                'show_retry': True
            })
        
        event = get_object_or_404(Event, id=payment_info['event_id'])
        
        if total_amount != float(event.price):
            return render(request, 'pages/event/payment_error.html', {
                'error_title': 'Amount Mismatch',
                'error_message': "Payment amount doesn't match ticket price. Please contact support.",
                'show_contact': True
            })
        
        user = get_object_or_404(CustomUser, id=payment_info['user_id'])
        
        ticket = PurchaseTicket.objects.create(
            ticket_id=transaction_uuid,
            event=event,
            user=user
        )
        
        event.book_ticket()
        
        del request.session[session_key]
        request.session.modified = True
        
        return render(request, "pages/event/ticket.html", {"ticket": ticket})
    
    except json.JSONDecodeError:
        return render(request, 'pages/event/payment_error.html', {
            'error_title': 'Invalid Data Format',
            'error_message': 'Received invalid payment data from eSewa.',
            'show_contact': True
        })
    
    except Exception:
        return render(request, 'pages/event/payment_failure.html')


def payment_failure(request):
    return render(request, "pages/event/payment_failure.html")
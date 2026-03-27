from django.db import models
from agro.models import Event
import uuid
from user.models import CustomUser
# Create your models here.

#--------------------------------Purchase Ticket----------------
import uuid
from django.db import models
from agro.models import Event
from user.models import CustomUser

class PurchaseTicket(models.Model):
    STATUS_PENDING  = 'pending'
    STATUS_COMPLETE = 'complete'
    STATUS_CHOICES  = [
        (STATUS_PENDING,  'Pending'),
        (STATUS_COMPLETE, 'Complete'),
    ]

    ticket_id     = models.UUIDField(default=uuid.uuid4, unique=True)
    event         = models.ForeignKey(Event, on_delete=models.CASCADE)
    user          = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    # --- new fields ---
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING      # every ticket starts as pending
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2            # stores the price at time of purchase
    )

    def __str__(self):
        return f"'{self.ticket_id}' - purchased by '{self.user.username}' [{self.status}]"
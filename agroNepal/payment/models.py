from django.db import models
from agro.models import Event
import uuid
from user.models import CustomUser
# Create your models here.

#--------------------------------Purchase Ticket----------------
class PurchaseTicket(models.Model):
  ticket_id = models.UUIDField(default=uuid.uuid4)
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  purchase_date = models.DateTimeField( auto_now_add=True)
  
  def __str__(self):
    return f"'{self.ticket_id}' - id ticket is purchase by the '{self.user.username}'"
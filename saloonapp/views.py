from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Saloon
from .models import Service
from .models import Master
from .models import Note


def index(request):
    context = {
        'saloons': Saloon.objects.all(),
        'services': Service.objects.all(),
        'masters': Master.objects.select_related('speciality').all(),
    }
    return render(request, template_name='index.html', context=context)


@login_required
def notes(request):
    user = request.user
    notes = Note.objects.select_related('saloon', 'service', 'master', 'payment', 'promo').filter(user=user)
    total_price = Decimal(0)
    payment_ids = []
    for note in notes:
        total_price += note.payment.get_total_price()
        payment_ids.append(str(note.payment.pk))
    context = {
        'notes': notes,
        'total': {
            'price': total_price,
            'payments': ','.join(payment_ids)
        }
    }
    return render(request, template_name='notes.html', context=context)

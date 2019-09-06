from django.shortcuts import render
from .models import Loan, DayCharge, BodyHistory
from django.db.models import Sum, Max, F, Count


def first_task(request):

    first = Loan.objects.values('id', 'bodyhistory__body')\
        .annotate(total_charges=Sum('daycharge__summ'), last_charge_date=Max('bodyhistory__history_date'))\
        .order_by('last_charge_date')

    second = DayCharge.objects.annotate(summ_mult=F('summ')*F('loan_id')/100)

    third = Loan.objects.values('id', 'summ_initial')\
        .annotate(period=Count('daycharge__charge_date', distinct=True)-2)

    return render(request, 'first_task.html', {'first': first, 'second': second, "third": third})

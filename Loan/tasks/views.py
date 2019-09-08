from django.shortcuts import render
from .models import Loan, DayCharge, BodyHistory
from django.db.models import Sum, Max, F, Count, Min


def first_task(request):
    # 1st and 4th in process
    first = Loan.objects.select_related()\
        .annotate(total_charges=F('daycharge__summ')*Count('daycharge__charge_date', distinct=True), last_charge_date=Max('daycharge__charge_date'),
                  bodyhistory__body=F('bodyhistory__body'))\
        .order_by('last_charge_date')

    second = DayCharge.objects.annotate(summ_mult=F('summ')*F('loan_id')/100)

    third = Loan.objects.values('id', 'summ_initial')\
        .annotate(period=Count('daycharge__charge_date', distinct=True)-2)
    fourth = Loan.objects.annotate(chargings_summ=F('daycharge__summ')*Count('daycharge__charge_date', distinct=True))\
        .values('chargings_summ', 'bodyhistory__history_date', 'bodyhistory__body', 'bodyhistory__id') \
        .order_by('bodyhistory__history_date')

    fifth_1 = Loan.objects.select_related()\
        .annotate(summ_lower_initial=Sum('daycharge__summ'))\
        .filter(summ_lower_initial__gt=F("summ_initial"))
    fifth_2 = Loan.objects.select_related()\
        .annotate(summ_lower_initial=Sum('daycharge__summ'))\
        .filter(summ_lower_initial__lt=1000)
    fifth_3 = Loan.objects.select_related()\
        .annotate(first_in_2018=Min('bodyhistory__history_date'))\
        .filter(bodyhistory__history_date__lte='2018-12-31',
                bodyhistory__history_date__gte='2018-01-01')
    fifth_4 = Loan.objects.select_related()\
        .annotate(summ_lower_initial=Sum('daycharge__summ'))\
        .filter(summ_lower_initial__gt=F("summ_initial"), summ_lower_initial__lt=1000) \
        .annotate(first_in_2018=Min('bodyhistory__history_date'))\
        .filter(bodyhistory__history_date__lte='2018-12-31',
                bodyhistory__history_date__gte='2018-01-01')

    return render(request, 'first_task.html',
                  {'first': first, 'second': second,
                   "third": third, "fourth": fourth,
                   "fifth_1": fifth_1, "fifth_2": fifth_2, "fifth_3": fifth_3, "fifth_4": fifth_4})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item, Memorandum, TravelOrder, SpecialOrder, CommunicationLetter, MOAU, MOAUParties, MOAUSignatories
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.shortcuts import render

# List all items

def item_list(request):
    # Gather all document types and tag them for template logic
    memos = list(Memorandum.objects.all())
    for m in memos:
        m._doc_type = 'memorandum'
    tos = list(TravelOrder.objects.all())
    for t in tos:
        t._doc_type = 'travelorder'
    sos = list(SpecialOrder.objects.all())
    for s in sos:
        s._doc_type = 'specialorder'
    cls = list(CommunicationLetter.objects.all())
    for c in cls:
        c._doc_type = 'commletter'
    moa_us = list(MOAU.objects.all())
    for mo in moa_us:
        mo._doc_type = 'moau'
    # Combine all into one list for display
    items = memos + tos + sos + cls + moa_us
    # Sort by date if possible (fallback to id)
    def get_date(obj):
        return getattr(obj, 'memo_date', None) or getattr(obj, 'date_issued', None) or getattr(obj, 'so_date', None) or getattr(obj, 'approved_date', None) or getattr(obj, 'id', 0)
    items = sorted(items, key=get_date, reverse=True)
    return render(request, 'pages/item_list.html', {'items': items})

# Create a new item

def item_create(request):
    if request.method == 'POST':
        # Only create Item if both name and description are provided
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            Item.objects.create(name=name, description=description)
            return redirect('item_list')
        else:
            # Show error if name is missing
            return render(request, 'pages/item_form.html', {'error': 'Name is required.'})
    return render(request, 'pages/item_form.html')

# Update an item

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.save()
        return redirect('item_list')
    return render(request, 'pages/item_form.html', {'item': item})

# Delete an item

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'pages/item_confirm_delete.html', {'item': item})

# Create your views here.

def home(request):
   return render(request, 'pages/home.html')

def search(request):
    query = request.GET.get('q', '')
    results = None
    if query:
        results = Item.objects.filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )
    return render(request, 'pages/search.html', {'results': results, 'request': request})

def to_form(request):
    if request.method == 'POST':
        to_no = request.POST.get('to_no')
        series_of = request.POST.get('series_of')
        date_issued = request.POST.get('date_issued')
        place = request.POST.get('place')
        inclusive_dates = request.POST.get('inclusive_dates')
        mode_trans = request.POST.get('mode_trans')
        purpose = request.POST.get('purpose')
        remarks = request.POST.get('remarks')
        approved_by = request.POST.get('approved_by')
        TravelOrder.objects.create(
            to_no=to_no,
            series_of=series_of,
            date_issued=date_issued,
            place=place,
            inclusive_dates=inclusive_dates,
            mode_trans=mode_trans,
            purpose=purpose,
            remarks=remarks,
            approved_by=approved_by
        )
        return render(request, 'pages/to_form.html', {'success': True})
    return render(request, 'pages/to_form.html')

def so_form(request):
    if request.method == 'POST':
        so_no = request.POST.get('so_no')
        so_date = request.POST.get('so_date')
        so_subject = request.POST.get('so_subject')
        so_content = request.POST.get('so_content')
        so_for = request.POST.get('so_for')
        so_signedby = request.POST.get('so_signedby')
        so_file = request.FILES.get('so_file')
        SpecialOrder.objects.create(
            so_no=so_no,
            so_date=so_date,
            so_subject=so_subject,
            so_content=so_content,
            so_for=so_for,
            so_signedby=so_signedby,
            so_file=so_file
        )
        return render(request, 'pages/so_form.html', {'success': True})
    return render(request, 'pages/so_form.html')

def cl_form(request):
    if request.method == 'POST':
        letter_to = request.POST.get('letter_to')
        letter_from = request.POST.get('letter_from')
        subject = request.POST.get('subject')
        received_by = request.POST.get('received_by')
        received_date = request.POST.get('received_date')
        letter_notedby = request.POST.get('letter_notedby')
        letter_recom_approval = request.POST.get('letter_recom_approval')
        letter_approved_by = request.POST.get('letter_approved_by')
        letter_file = request.FILES.get('letter_file')
        CommunicationLetter.objects.create(
            letter_to=letter_to,
            letter_from=letter_from,
            subject=subject,
            received_by=received_by,
            received_date=received_date,
            letter_notedby=letter_notedby,
            letter_recom_approval=letter_recom_approval,
            letter_approved_by=letter_approved_by,
            letter_file=letter_file
        )
        return render(request, 'pages/cl_form.html', {'success': True})
    return render(request, 'pages/cl_form.html')

def moau_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        approved_date = request.POST.get('approved_date')
        objective = request.POST.get('objective')
        notarized_by = request.POST.get('notarized_by')
        notarized_date = request.POST.get('notarized_date')
        moau_file = request.FILES.get('moau_file')
        MOAU.objects.create(
            title=title,
            approved_date=approved_date,
            objective=objective,
            notarized_by=notarized_by,
            notarized_date=notarized_date,
            moau_file=moau_file
        )
        return render(request, 'pages/moau_form.html', {'success': True})
    return render(request, 'pages/moau_form.html')

def moau_p_form(request):
    if request.method == 'POST':
        moau_no = request.POST.get('moau_no')
        agency = request.POST.get('agency')
        represented_by = request.POST.get('represented_by')
        position = request.POST.get('position')
        address = request.POST.get('address')
        referred_to_as = request.POST.get('referred_to_as')
        moau = MOAU.objects.get(pk=moau_no)
        MOAUParties.objects.create(
            moau_no=moau,
            agency=agency,
            represented_by=represented_by,
            position=position,
            address=address,
            referred_to_as=referred_to_as
        )
        return render(request, 'pages/moau-p_form.html', {'success': True})
    return render(request, 'pages/moau-p_form.html')

def moau_s_form(request):
    if request.method == 'POST':
        moau_no = request.POST.get('moau_no')
        signed_by = request.POST.get('signed_by')
        position = request.POST.get('position')
        agency = request.POST.get('agency')
        moau = MOAU.objects.get(pk=moau_no)
        MOAUSignatories.objects.create(
            moau_no=moau,
            signed_by=signed_by,
            position=position,
            agency=agency
        )
        return render(request, 'pages/moau-s_form.html', {'success': True})
    return render(request, 'pages/moau-s_form.html')

def item_form(request):
    if request.method == 'POST':
        memo_no = request.POST.get('memo_no')
        memo_date = request.POST.get('memo_date')
        memo_to = request.POST.get('memo_to')
        memo_to_pos = request.POST.get('memo_to_pos')
        memo_thru = request.POST.get('memo_thru')
        memo_thru_pos = request.POST.get('memo_thru_pos')
        memo_from = request.POST.get('memo_from')
        memo_from_pos = request.POST.get('memo_from_pos')
        memo_subject = request.POST.get('memo_subject')
        memo_content = request.POST.get('memo_content')
        memo_recomm_by = request.POST.get('memo_recomm_by')
        memo_approved_by = request.POST.get('memo_approved_by')
        # File upload handling
        memo_file = request.FILES.get('dropzone-file') or request.FILES.get('memo_file')
        # Save to Memorandum model
        Memorandum.objects.create(
            memo_no=memo_no,
            memo_date=memo_date,
            memo_to=memo_to,
            memo_to_pos=memo_to_pos,
            memo_thru=memo_thru,
            memo_thru_pos=memo_thru_pos,
            memo_from=memo_from,
            memo_from_pos=memo_from_pos,
            memo_subject=memo_subject,
            memo_content=memo_content,
            memo_recomm_by=memo_recomm_by,
            memo_approved_by=memo_approved_by,
            memo_file=memo_file
        )
        return render(request, 'pages/item_form.html', {'success': True})
    return render(request, 'pages/item_form.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'pages/login.html', {'form': {}, 'error': True})
    return render(request, 'pages/login.html', {'form': {}})

def logout_view(request):
    logout(request)
    return redirect('login')

def reports(request):
    # List of all document models and their display names
    from .models import Memorandum, TravelOrder, SpecialOrder, CommunicationLetter, MOAU
    doc_models = [
        (Memorandum, 'Memorandum', 'memo_no'),
        (TravelOrder, 'Travel Order', 'to_no'),
        (SpecialOrder, 'Special Order', 'so_no'),
        (CommunicationLetter, 'Communication Letter', 'letter_no'),
        (MOAU, 'MOAU', 'moau_no'),
    ]
    doc_counts = []
    for model, name, pk in doc_models:
        doc_counts.append({'type': name, 'count': model.objects.count()})

    # Monthly report (all types combined)
    # We'll use Memorandum as an example; repeat for all models and sum per month
    from collections import Counter
    monthly_counter = Counter()
    for model, _, pk in doc_models:
        qs = model.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count(pk)).order_by('month')
        for row in qs:
            if row['month']:
                key = row['month'].strftime('%Y-%m')
                monthly_counter[key] += row['count']
    # Prepare data for chart.js
    months = sorted(monthly_counter.keys())
    counts = [monthly_counter[m] for m in months]
    monthly_data = {'labels': months, 'counts': counts}

    return render(request, 'pages/reports.html', {
        'doc_counts': doc_counts,
        'monthly_data': monthly_data,
    })

def user_document_list(request):
    # For now, use the same logic as item_list
    memos = list(Memorandum.objects.all())
    for m in memos:
        m._doc_type = 'memorandum'
    tos = list(TravelOrder.objects.all())
    for t in tos:
        t._doc_type = 'travelorder'
    sos = list(SpecialOrder.objects.all())
    for s in sos:
        s._doc_type = 'specialorder'
    cls = list(CommunicationLetter.objects.all())
    for c in cls:
        c._doc_type = 'commletter'
    moa_us = list(MOAU.objects.all())
    for mo in moa_us:
        mo._doc_type = 'moau'
    items = memos + tos + sos + cls + moa_us
    def get_date(obj):
        return getattr(obj, 'memo_date', None) or getattr(obj, 'date_issued', None) or getattr(obj, 'so_date', None) or getattr(obj, 'approved_date', None) or getattr(obj, 'id', 0)
    items = sorted(items, key=get_date, reverse=True)
    return render(request, 'pages/user-document_list.html', {'items': items})

def user_notification(request):
    # Example: static notifications for UI demo
    notifications = [
        {
            'doc_id': 'MEMO-001',
            'type': 'Memorandum',
            'subject': 'Subject about you',
            'related': 'You are the recipient',
            'date': '2025-06-27',
        },
        {
            'doc_id': 'TO-002',
            'type': 'Travel Order',
            'subject': 'Trip to Manila',
            'related': 'You are included',
            'date': '2025-06-25',
        },
    ]
    return render(request, 'pages/user-notification.html', {'notifications': notifications})

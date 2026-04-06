from django.shortcuts import render, redirect
from .models import Expense
from django.db.models import Sum

def index(request):
    # 1. Search Logic
    search_query = request.GET.get('search', '')

    # 2. Add Expense Logic (POST request)
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        
        if title and amount:
            Expense.objects.create(title=title, amount=amount, category=category)
        
        return redirect('index')

    # 3. Filtering and Fetching Data
    if search_query:
        expenses = Expense.objects.filter(title__icontains=search_query).order_by('-date')
    else:
        
        expenses = Expense.objects.all().order_by('-date')

    # 4. Total Calculation
    total_data = expenses.aggregate(Sum('amount'))
    total_amount = total_data['amount__sum'] if total_data['amount__sum'] else 0
    
    return render(request, 'expenses/index.html', {
        'expenses': expenses,
        'total_amount': total_amount,
        'search_query': search_query
    })

def delete_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect('index')
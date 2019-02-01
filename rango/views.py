from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.http import HttpResponseRedirect
from rango.forms import PageForm
# Create your views here.

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]

    page_list = Page.objects.order_by('-views')[:5]

    context = {'categories': category_list,'pages':page_list}

    return render(request,'rango/index.html',context=context)

def about(request):
    context = {'yourname':'Richard Nemeth'}
    return render(request,'rango/about.html',context=context)

def show_category(request,category_name_slug):
    context_dict={}
    print(category_name_slug)
    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages']=pages
        context_dict['category']= category

    except Category.DoesNotExist:
        context_dict['pages']=None
        context_dict['category'] = None
    return render(request,'rango/category.html',context = context_dict)

def add_category(request):

    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return HttpResponseRedirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html',{'form':form})

def add_page(request,category_name_slug):

    try:
        category = Category.objects.get(slug=category_name_slug.lower())

    except Category.DoesNotExist :
        category = None
    print(category)
    form = PageForm()

    if request.method=="POST":
        print('hello')
        form = PageForm(request.POST)
        if form.is_valid():
            print('mate')
            if category:
                print('mate')
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return HttpResponseRedirect('/rango/')
            else:
                print(form.errors)
    conext = {'form': form, 'category': category}
    return render(request,'rango/add_page.html',conext)

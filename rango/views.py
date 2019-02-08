from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.http import HttpResponseRedirect
from rango.forms import PageForm
from rango.forms import UserProfileForm, UserForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
# Create your views here.

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    request.session.set_test_cookie()
    context = {'categories': category_list,'pages':page_list}

    visitor_cookie_handler(request)
    context['visits'] = request.session['visits']

    response = render(request,'rango/index.html',context=context)

    return response

def about(request):
    context = {'yourname':'Richard Nemeth'}
    if(request.session.test_cookie_worked()):
        print('TEST COOKIE WORKED!')
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


def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)

            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True



        else:
            print(user_form.errors, profile_form.errors)
    else:

        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
        'rango/register.html',
        {'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:

            if user.is_active:

                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Your Rango account is disabled")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:

        return render(request,'rango/login.html')

@login_required
def restricted(request):
    return render(request,'rango/restricted.html',{})

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):

    visits = int(get_server_side_cookie(request,'visits','1'))

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
        # Update/set the visits cookie
    request.session['visits'] = visits

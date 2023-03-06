from django.shortcuts import render, redirect
from .models import Cat, Toy, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .forms import FeedingForm
import uuid #python package for creating unique identifiers
import boto3 # what we'll use to connect to s3
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET = settings.S3_BUCKET
S3_BASE_URL = settings.S3_BASE_URL
# Create your views here.
# View functions match urls to code (like controllers in Express)
# Define our home view function
def home(request):
    # Include an .html file extension - unlike when rendering EJS templates
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#index route for cats
@login_required
def cats_index(request):
    # Just like we passed data to our templates in express
    # We pass data to our templates through our view functions
    # We can gather relations from SQL using our model methods
    # cats = Cat.objects.all()
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', { 'cats': cats })

#Detail route for cats
# Cat_id is defined, expecting an integer, in our URL
@login_required
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # Get the toys the cat doesn't have...
    # First, create a list of the toy ids that the cat DOES have
    id_list = cat.toys.all().values_list('id')
    # Now we can query for toys whose ids are not in the list using exclude
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat, 'feeding_form': feeding_form,
        # Add the toys to be displayed
        'toys': toys_cat_doesnt_have
    })

@login_required
def add_feeding(request, cat_id):
    # Create a model form instance form the data in request.POST
    form = FeedingForm(request.POST)
    # Validate form (does it match our data)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail', cat_id=cat_id)




class CatCreate(CreateView):
    model = Cat
    #The fields attribute if required for a create view
    # fields = '__all__'
    # Same as below =>
    fields = ['name', 'breed', 'description', 'age']
    # success_url = "/cats/{cat_id}"
    def form_valid(self, form):
        # we can assign teh logged in user's data(id) to the cat's create form
        form.instance.user = self.request.user
        return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    # custom fields to disallow renaming a cat
    fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    #success url, index page
    success_url = '/cats/'

# ToyList
class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/detail.html'
# ToyCreate
class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ['name', 'color']

    # define what the inherited method is_valid does (we'll update this later)
    def form_valid(self, form):
        #use later, implement now
        #we'll need this when we add auth
        #Super allows for the original inherited CreateView function to work as it was intended
        return super().form_valid(form)
# ToyUpdate
class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

# ToyDelete
class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

@login_required
def assoc_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
def add_photo(request, cat_id):
    #photo_file will be the name attribute of our form input
    photo_file = request.FILES.get('photo-file', None)
    #use conditional logic to make sure file is present
    if photo_file:
        #if present, use to create a reference to the boto3 client
        s3 = boto3.client(
            's3', 
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
        # create unique key for our photos 
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            #if success
            s3.upload_fileobj(photo_file, S3_BUCKET, key)
            #build full url string to uplaod to s3
            url = f"{S3_BASE_URL}{S3_BUCKET}/{key}"
            # use that photo location to create Photo model
            photo = Photo(url=url, cat_id=cat_id)
            #save instance
            photo.save()
        except Exception as error:
            print('Error uploading photo', error)
            return redirect('detail', cat_id=cat_id)
        
    return redirect('detail', cat_id=cat_id)

def signup(request):
    # this view is going to be like our class-based-views
    # this is going to be able to handle a GET and a POST request
    error_message = ''
    if request.method == 'POST':
        # this is how to create a user form object that includes data from the browser
        form = UserCreationForm(request.POST)
        # now we check validity of the form and handle our success and error situations
        if form.is_valid():
            # we'll add the user to the database
            user = form.save()
            # then we'll log the user in
            login(request, user)
            # redirect to our index page
            return redirect('index')
        else:
            error_message = 'Invalid signup - try again'
    # a bad POST or GET request will render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
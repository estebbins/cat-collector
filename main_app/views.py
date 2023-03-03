from django.shortcuts import render, redirect
from .models import Cat
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm
# temporary cats for building templates
# cats = [
#     {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry lil demon', 'age': 12},
#     {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 3},
#     {'name': 'Tubbs', 'breed': 'ragdoll', 'description': 'pretty floppy', 'age': 0},
# ]

# Create your views here.
# View functions match urls to code (like controllers in Express)
# Define our home view function
def home(request):
    # Include an .html file extension - unlike when rendering EJS templates
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#index route for cats
def cats_index(request):
    # Just like we passed data to our templates in express
    # We pass data to our templates through our view functions
    # We can gather relations from SQL using our model methods
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', { 'cats': cats })

#Detail route for cats
# Cat_id is defined, expecting an integer, in our URL
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    #Instantiate feeding form to be rendered in the template
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form })

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
    fields = '__all__'
    # Same as below =>
    # fields = ['name', 'breed', 'description', 'age']
    # success_url = "/cats/{cat_id}"

class CatUpdate(UpdateView):
    model = Cat
    # custom fields to disallow renaming a cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    #success url, index page
    success_url = '/cats/'


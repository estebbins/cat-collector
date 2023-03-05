from django.shortcuts import render, redirect
from .models import Cat, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
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

class CatUpdate(UpdateView):
    model = Cat
    # custom fields to disallow renaming a cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    #success url, index page
    success_url = '/cats/'

# ToyList
class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'
# ToyCreate
class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

    # define what the inherited method is_valid does (we'll update this later)
    def form_valid(self, form):
        #use later, implement now
        #we'll need this when we add auth
        #Super allows for the original inherited CreateView function to work as it was intended
        return super().form_valid(form)
# ToyUpdate
class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

# ToyDelete
class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

def assoc_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)
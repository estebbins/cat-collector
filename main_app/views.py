from django.shortcuts import render

# temporary cats for building templates
cats = [
    {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry lil demon', 'age': 12},
    {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 3},
    {'name': 'Tubbs', 'breed': 'ragdoll', 'description': 'pretty floppy', 'age': 0},
]

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
    return render(request, 'cats/index.html', { 'cats': cats })
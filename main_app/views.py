from django.shortcuts import render

# Create your views here.
# View functions match urls to code (like controllers in Express)
# Define our home view function
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')
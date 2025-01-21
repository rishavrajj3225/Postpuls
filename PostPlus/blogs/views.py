from django.shortcuts import render
from .forms import blogForm, UserRegistrationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404 , redirect
from .models import blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def home(request):
    return render(request, 'index.html')

def blog_list(request):
    blogs= blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})
@login_required
def blog_create(request):
    if request.method == 'POST':
        form= blogForm(request.POST, request.FILES)
        if form.is_valid():
           blog= form.save(commit=False)
           blog.user= request.user    #assigning the current user to the blog
           blog.save()
           return HttpResponseRedirect('/blogs/')    #redirecting to the blog list page
    else:
        form= blogForm()
    return render(request, 'blog_form.html', {'form': form})
@login_required
def blog_update(request, blog_id):
    blogs= get_object_or_404(blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        form= blogForm(request.POST , request.FILES , instance=blogs)
        if form.is_valid():
            form.save(commit=False)
            blogs.user= request.user
            blogs.save()
            return HttpResponseRedirect('/blogs/')
    else:
        form= blogForm(instance=blogs)
    return render(request, 'blog_form.html', {'form': form})
@login_required
def blog_delete(request, blog_id):
    # Fetch the blog instance for the current user
    blogs = get_object_or_404(blog, pk=blog_id, user=request.user)
    
    if request.method == 'POST':
        print("POST request received for deleting the blog")  # Debug
        blogs.delete()
        return redirect('allBlogs')
    
    return render(request, 'blog_confirm_delete.html', {'blogs': blogs})



def blog_detail(request,blog_id):
    blogs= get_object_or_404(blog,pk=blog_id)
    return render(request, 'blog_detail.html', {'blog':blogs})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('allBlogs')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
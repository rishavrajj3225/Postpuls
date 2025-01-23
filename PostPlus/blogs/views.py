from .forms import blogForm, UserRegistrationForm, editUserProfile
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 , redirect
from .models import blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get('API_KEY'))
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
            auth_login(request, user)
            return redirect('allBlogs')
    else:
        initial_data={'username':'','password1':'','password2':''}
        form = UserRegistrationForm(initial=initial_data)
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  
            return redirect('allBlogs') 
    else:
        intial_data={'username':'','password':''}
        form = AuthenticationForm(initial=intial_data)      
    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_blog_list(request):
    blogs = blog.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_blog_list.html', {'blogs': blogs})

def profile(request):
    return render(request, 'user_account.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = editUserProfile(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_account')  
    else:
        user_form = editUserProfile(instance=request.user)

    return render(request, 'edit_profile.html', {'user_form': user_form})

def aiAnalyzer(request, blog_id):
    user_input = request.GET.get('user_input', '')  

    blogs = get_object_or_404(blog, id=blog_id)  
    blog_content = blogs.content

    system_input = """When user gives you a command like summarize the blog, Extract important information from the blog and present it in blog, extract the emphasizing point form input system. like summarize, important, extract, emphasizing or similar word you would extract that word and return and add "remaninigWork " before that response like "remaningWork important" here important is extracted word other wise use your own algorith to answer that query and do not display "There is no command in "hii how are you" that matches the keywords "summarize, important, extract, emphasizing".  Therefore, I will use my own algorithm to respond." this type of answer also do not show "My response: ***" this only show ***  where *** is your response and if any one ask you question about yourself then reply in your own way like for question "how are you?","heyy", "hii",. one more case where one have ask more than one question like "how are you can you summarize the blog" then you have to answer the first question and then answer the second question. like in this example answer for "how are you" and then answer for "can you summarize the blog" answer will be like "Hey! I'm doing well, thanks for asking.  How are you?" and then answer for can you summarize the blog ."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{system_input}\n{user_input}")

    if "remaningWork" not in response.text:
        answer = response.text
    else:
        todo = response.text.replace("remaningWork", "").strip()
        response = model.generate_content(f"{blog_content}\n{todo}")
        answer = response.text

    # Render the AI response in the template
    return render(request, 'aianalyzers.html', {'answer': answer, 'blog': blog, "blog_id": blog_id})





from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
import ezgmail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

def home(request):
    allpost = Post.objects.all()
    allPosts = allpost.reverse()[0:5]
    # print(allPosts[0:5:1])
    params = {'allPosts' : allPosts}
    return render(request, 'home/home.html', params)


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name)<2 or len(email)<5 or len(phone)<5 or len(content)<8:
            messages.error(request, "Please Fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your response has been recorded. Thanks for contacting us !!")
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query)>80:
        allPosts = {}
        messages.error(request, "No search results found")

    else:
        allPostsTitle =   Post.objects.filter(title__icontains=query)
        allPostsContent =   Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    params = {'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html',params)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']   
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        

        if len(username) > 10:
            messages.error(request, "Username Must be less than 10 Characters")
            return redirect('/')
        if not username.isalnum():
            messages.error(request, "Username Must contain only letters and numbers")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('/')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "You have Signed Up Succesfully")
        print(username, pass1, pass2)
        return redirect('/')
    else:
        return HttpResponse("404 - Not Found")


def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['usernamelogin']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Sucessfully")
            return redirect('/')

        else:
            messages.error(request, "Please enter username and password correctly")
            return redirect('/')

    
    return HttpResponse("404 - Login Page Not Found")
        

def handleLogout(request):
    logout(request)
    messages.success(request, "You have been Logged Out Succesfully")
    return redirect('home') 
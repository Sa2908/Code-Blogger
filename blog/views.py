from typing import Pattern
from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.                   

def blogHome(request):
    # return HttpResponse("Blog Home Page")
    allPosts = Post.objects.all()
    allPosts2 = reversed(list(allPosts))
    context = {'allPosts': allPosts2}
    # print(type(allPosts))

    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        
        else:
            replyDict[reply.parent.sno].append(reply)


    context = {'post': post, 'comments': comments, 'replyDict' : replyDict}
    return render(request, 'blog/blogPost.html', context)


def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your Comment has been Posted successfully")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

            comment.save()
            messages.success(request, "Your Reply has been Posted successfully")


    return redirect(f'/blog/{post.slug}')


def create(request):

    return render(request, 'blog/blogCreate.html')


def postBlog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('user')
        slug = title.replace(' ', '-')
        post = Post(title=title, content=content, author=author, slug=slug)
        post.save()

    
    return redirect(f'/blog/{slug}')
        
from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def blogHome(request):
    allPosts = Post.objects.all().order_by('-views')
    lst = []
    for i in allPosts:
        context = {"allPosts": allPosts, "lst":lst}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    userlist = User.objects.all()
    
    post = Post.objects.filter(slug=slug).first()
    post.views += 1
    post.save()
    allcomments = BlogComment.objects.all()
    parentSno = request.POST.get("parentSno")
    replySno = request.POST.get("replySno")
    comments = BlogComment.objects.filter(post=post)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    
    '''output of above line: {29: [<BlogComment: hi this is relp... by  nishant>, <BlogComment: second time rep... by  nishant>], 31: [<BlogComment: hello 2 reply
     by  nishant>, <BlogComment: 2 reply of 2 co... by  nishant>]}'''
    replys = BlogComment.objects.filter(parent=replySno)

    context = {"post": post, "comments": comments, "allcomments": allcomments,'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', context)



def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        replytext = request.POST.get("replybox")

        if not replytext:
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "U just commented")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            print(parent.sno, "parent sno")
            ''' I was facing error because this else condition true if u posting reply and in Form tag in the blogPost.html had not postSno hidden input tag in it both comments and reply has post=post variable to save in BlogComment model and that post variable is come from serial number postSno so post=post is common in both condition either to post comment or reply so both Form tag should have postSno '''
            comment = BlogComment(comment=replytext, user=user, post=post, parent=parent)
            comment.save()
            print(comment.parent.sno, "compar")
            print(comment.sno, "comment sno")
            messages.success(request, "U just reply")

    return redirect(f"/blog/{post.slug}")

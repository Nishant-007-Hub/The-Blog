from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from Blogger.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.
def blank(request):
    # return HttpResponse("this is blank page") 
    allPosts = Post.objects.all().order_by('-views')
    context = {"allPosts":allPosts}
    return render(request,'Home/home.html',context)

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["content"]
        if name != "" or email!= "" or phone != "":
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            # messages.add_message(request, messages.INFO, 'Hello world.')
            messages.success(request, 'Contact form has been submitted successfully')
        else:
            messages.error(request, 'plz fill info correctly')

    return render(request,'home/contact.html')

    # return HttpResponse("this is contact page") 

def about(request):
    return render(request, 'home/about.html')

def handlesignup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.warning(request, "!password not match")
            return redirect('blank')

        else:
            myuser = User.objects.create_user(username, email, pass2, first_name = fname,last_name = lname)
            myuser.save()
            messages.success(request, " Your Account has been successfully created")
            return redirect('blank')
    else:
        return HttpResponse("404 - Not found")



def handleslogin(request):
    if request.method == "POST":
        username = request.POST['loginusername']
        loginpassword = request.POST['loginpass']

        user = authenticate(username=username, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}!!")
            return redirect("blank")
        else:
            messages.error(request, "!! Invalid credentials")
            return redirect("blank")

    return HttpResponse("404 - Not found")


def handleslogout(request):
    logout(request)
    messages.success(request, " !! Successfully Logout")
    return redirect("blank")
    return HttpResponse("Logout")


def search(request):
# --------------------------------method-1----------------------------------------
    query = request.GET.get("query").lower()
    posttitle = Post.objects.filter(title__icontains=query)
    postcontent = Post.objects.filter(content__icontains=query)
    postauthor = Post.objects.filter(author__icontains=query)
    searchedlist = posttitle.union(
        postcontent, postauthor)

    # --------------------------------method-2----------------------------------------
    # allPost = Post.objects.all()
    # searchedlist = []
    # for post in allPost:
    #     if query in post.title or query in post.content or query in post.author:
    #         searchedlist.append(post)

    string=[]

    if searchedlist.count()==0:
        string.append("No such results found")
        messages.warning(request,f"Your search query \"{query}\" no such results found did not match any documents")
    
    context = {"results":searchedlist, "query":query , "nolist": string}

    return render(request,'home/search.html', context)

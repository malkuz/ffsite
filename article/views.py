from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def detail(request, id):
    return HttpResponse("<h3>Detail:</h3> <hr> " + str(id))

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url = "user:login")
def add_article(request):
    print(request.FILES)
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale başarıyla kaydedildi.")
        return redirect("index")
    return render(request, "add_article.html", {"form":form})

def viewArticle(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    return render(request,"viewArticle.html", {"article":article, "comments":comments})

@login_required(login_url = "user:login")
def edit(request, id):
    edit_article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance = edit_article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale başarıyla güncellendi.")
        return redirect("article:dashboard")
    return render(request, "edit.html", {"article":edit_article, "form":form})

@login_required(login_url = "user:login")
def delete(request, id):
    del_article = get_object_or_404(Article, id=id)
    del_article.delete()
    messages.success(request, "Makale silindi.")
    return redirect("article:dashboard")

def allArticles(request):
    if request.method == "GET":
        articles = Article.objects.all()
        return render(request, "articles.html", {"articles":articles})
    else:
        articles = Article.objects.filter(content__contains = request.POST["search"])
        messages.success(request, str(len(articles)) + " adet makale bulundu.")
        return render(request, "articles.html", {"articles":articles})

def addComment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        comment = Comment(article=article, comment_author=comment_author, comment_content=comment_content)
        comment.save()
    return redirect("/articles/view/" + str(id))

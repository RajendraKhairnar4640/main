
from django.shortcuts import render,HttpResponseRedirect,redirect,get_object_or_404
from .forms import RegisterForm,NewPostForm,NewCommentForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Post, Comments,Like
from django.views.generic import ListView, UpdateView, DeleteView,CreateView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.views import View

class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('register')
    template_name = 'myapp/registration.html'
    success_message = "%(username)s was created successfully"

    def form_valid(self, form):
        messages.success(self.request, f"Account created successfully")
        return super().form_valid(form)

class LoginView(View):
    def get(self,request):
        return render(request,'myapp/userlogin.html',{'form':AuthenticationForm})

    def post(self,request):
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
        return render(request,'myapp/userlogin.html',{'form':form})

def user_dashboard(request):
    if request.user.is_authenticated:
        return render(request,'myapp/user_dashboard.html')
    else:
        return HttpResponseRedirect('/login/')

@login_required(login_url='login')
def create_post(request):
    user = request.user
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_name = user
            data.save()
            messages.success(request,f'Posted Successfully')
            return redirect('home')
    else:
        form = NewPostForm()
    return render(request,'myapp/create_post.html',{'form':form})

@login_required(login_url='login')
def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    user = request.user
    is_liked = Like.objects.filter(user=user,post=post)
    
    if request.method == "POST":
        fm = NewCommentForm(request.POST)
        if fm.is_valid():
            data = fm.save(commit=False)
            data.post = post
            data.username = user
            data.save()
            return redirect('post-detail',pk=pk)
    else:
        fm = NewCommentForm()
    return render(request,'myapp/post_detail.html',{'post':post,'is_liked':is_liked,'form':fm})

class PostListView(ListView):
	model = Post
	template_name = 'myapp/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5
	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			liked = [i for i in Post.objects.all() if Like.objects.filter(user = self.request.user, post=i)]
			context['liked_post'] = liked
		return context

@login_required(login_url='login')
def like(request):
	post_id = request.GET.get("likeId", "")
	user = request.user
	post = Post.objects.get(pk=post_id)
	liked= False
	like = Like.objects.filter(user=user, post=post)
    
	if like:
		like.delete()
	else:
		liked = True
		Like.objects.create(user=user, post=post)
	resp = {
        'liked':liked
    }
	response = json.dumps(resp)
	return HttpResponse(response, content_type = "application/json")

@login_required(login_url='login')
def search_posts(request):
	query = request.GET.get('p')
	object_list = Post.objects.filter(tags__icontains=query)
	liked = [i for i in object_list if Like.objects.filter(user = request.user, post=i)]
	context ={
		'posts': object_list,
		'liked_post': liked
	}
	return render(request, "myapp/search_posts.html", context)

@login_required(login_url='login')
def post_delete(request,pk):
    post = Post.objects.get(pk=pk)
    if request.user==post.user_name:
        Post.objects.get(pk=pk).delete()
    return redirect('home')


class UserPostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'myapp/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super(UserPostListView, self).get_context_data(**kwargs)
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		liked = [i for i in Post.objects.filter(user_name=user) if Like.objects.filter(user = self.request.user, post=i)]
		context['liked_post'] = liked
		return context

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(user_name=user).order_by('-date_posted')


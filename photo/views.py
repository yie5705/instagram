from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from photo.models import Photo
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse


# Create your views here.
class PhotoList(ListView): 
    model = Photo
    template_name_suffix = '_list'

class PhotoCreate(CreateView):
    model = Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_create'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_update'
    success_url = '/'
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author !=request :
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else :
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'

class PhotoLike(View) :
    def get(self, request, *args, **kwargs) : #get 방식으로 왔을 때
        if not request.user.is_authenticated : #로그인 확인
            return HttpResponseForbidden(); #자료 숨기기
        else :
            if 'photo_id' in kwargs : 
                photo_id = kwargs['photo_id'] #photo_id를 확인
                photo = Photo.objects.get(pk=photo_id) #primary key 가지도록
                user = request.user 
                if user in photo.like.all() : #이미 user가 좋아요 한 사람에 있으면
                    photo.like.remove(user) #클릭했을 때 지움
                else : #user 가 좋아요 아직 안눌렀으면
                    photo.like.add(user) #유저 추가
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

class PhotoFavorite(View) :
    def get(self, request, *args, **kwargs) :
        if not request.user.is_authenticated :
            return HttpResponseForbidden()
        else :
            if 'photo_id' in kwargs :
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk = photo_id)
                user = request.user
                if user in photo.favorite.all() :
                    photo.favorite.remove(user)
                else :
                    photo.favorite.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
    
class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  #로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        #내가 좋아요한 글을 보여주기
        user = self.request.user
        queryset = user.like_post.all()
        return queryset

class PhotoFavoriteList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  #로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoFavoriteList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        #내가 저장한 글을 보여주기
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset

class PhotoMyList(ListView):
    model = Photo
    template_name = 'photo/photo_mylist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  #로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoMyList, self).dispatch(request, *args, **kwargs)


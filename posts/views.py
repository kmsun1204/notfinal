from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView  # new
from django.urls import reverse_lazy  # new

from .forms import ModelsForm, PhotoForm
from .models import Models, Photo

from django.core.paginator import Paginator


class ModelsPageView(ListView):
    model = Models
    template_name = 'model/model.html'
    paginate_by = 4
    queryset = Models.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.kwargs:
            return Models.objects.filter(category=self.kwargs['category']).order_by('-id')
        else:
            query = Models.objects.all().order_by('-id')
            return query


class CreateModelsView(CreateView):
    model = Models
    form_class = ModelsForm
    template_name = 'model/model_post.html'
    success_url = reverse_lazy('model')


def detail(request, model_id):
    post_detail = Models.objects.get(pk=model_id)
    return render(request, 'model/model_detail.html', {'post_detail': post_detail})


def delete(request, model_id):
    delete_model = Models.objects.get(id=model_id)
    delete_model.delete()
    return redirect('model')


def edit(request, model_id):
    model = Models.objects.get(id=model_id)

    if request.method == "POST":
        form = ModelsForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            model.title = form.cleaned_data['title']
            model.text = form.cleaned_data['text']
            model.image1 = form.cleaned_data['image1']
            model.image2 = form.cleaned_data['image2']
            model.image3 = form.cleaned_data['image3']
            model.image4 = form.cleaned_data['image4']
            model.image5 = form.cleaned_data['image5']
            model.save()
            return redirect('model_detail', model_id)

    else:
        form = ModelsForm()
    return render(request, 'model/model_edit.html', {'form': form, })


def filter_cute(request):
    post_cute = Models.objects.filter(category="큐티")
    cute_paginator = Paginator(post_cute, 4)
    cute_page = request.GET.get('page')
    cute_posts = cute_paginator.get_page(cute_page)
    return render(request, 'model/filter_cute.html', {'post_cute': post_cute,
                                                      'cute_posts': cute_posts,
                                                      'cute_paginator': cute_paginator, })


def filter_cool(request):
    post_cool = Models.objects.filter(category="청량")
    cool_paginator = Paginator(post_cool, 4)
    cool_page = request.GET.get('page')
    cool_posts = cool_paginator.get_page(cool_page)
    return render(request, 'model/filter_cool.html', {'post_cool': post_cool,
                                                      'cool_posts': cool_posts,
                                                      'cool_paginator': cool_paginator, })


def filter_bnw(request):
    post_bnw = Models.objects.filter(category="흑백사진")
    bnw_paginator = Paginator(post_bnw, 4)
    bnw_page = request.GET.get('page')
    bnw_posts = bnw_paginator.get_page(bnw_page)
    return render(request, 'model/filter_bnw.html', {'post_bnw': post_bnw,
                                                     'bnw_posts': bnw_posts,
                                                     'bnw_paginator': bnw_paginator, })


def filter_plus(request):
    post_plus = Models.objects.filter(category="플러스모델")
    plus_paginator = Paginator(post_plus, 4)
    plus_page = request.GET.get('page')
    plus_posts = plus_paginator.get_page(plus_page)
    return render(request, 'model/filter_plus.html', {'post_plus': post_plus,
                                                      'plus_posts': plus_posts,
                                                      'plus_paginator': plus_paginator, })


#####################################################


class PhotoPageView(ListView):
    model = Photo
    template_name = 'photo/photo.html'
    paginate_by = 4
    queryset = Photo.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.kwargs:
            return Photo.objects.filter(category=self.kwargs['category']).order_by('-id')
        else:
            query = Photo.objects.all().order_by('-id')
            return query


class PhotoCreatePostView(CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo/photo_post.html'
    success_url = reverse_lazy('photo')


def photo_detail(request, photo_id):
    photo_post_detail = Photo.objects.get(pk=photo_id)
    return render(request, 'photo/photo_detail.html', {'photo_post_detail': photo_post_detail})


def photo_delete(request, photo_id):
    delete_photo = Photo.objects.get(id=photo_id)
    delete_photo.delete()
    return redirect('photo')


def photo_edit(request, photo_id):
    photo = Photo.objects.get(id=photo_id)

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            photo.title = form.cleaned_data['title']
            photo.text = form.cleaned_data['text']
            photo.image1 = form.cleaned_data['image1']
            photo.image2 = form.cleaned_data['image2']
            photo.image3 = form.cleaned_data['image3']
            photo.image4 = form.cleaned_data['image4']
            photo.image5 = form.cleaned_data['image5']
            photo.save()
            return redirect('photo_detail', photo_id)

    else:
        form = PhotoForm()
    return render(request, 'photo/photo_edit.html', {'form': form, })


def photo_filter_cute(request):
    photo_post_cute = Photo.objects.filter(category="큐티")
    photo_cute_paginator = Paginator(photo_post_cute, 4)
    photo_cute_page = request.GET.get('page')
    photo_cute_posts = photo_cute_paginator.get_page(photo_cute_page)

    return render(request, 'photo/photo_filter_cute.html', {'photo_post_cute': photo_post_cute,
                                                            'photo_cute_posts': photo_cute_posts,
                                                            'photo_cute_paginator': photo_cute_paginator, })


def photo_filter_cool(request):
    photo_post_cool = Photo.objects.filter(category="청량")
    photo_cool_paginator = Paginator(photo_post_cool, 4)
    photo_cool_page = request.GET.get('page')
    photo_cool_posts = photo_cool_paginator.get_page(photo_cool_page)

    return render(request, 'photo/photo_filter_cool.html', {'photo_post_cool': photo_post_cool,
                                                            'photo_cool_posts': photo_cool_posts,
                                                            'photo_cool_paginator': photo_cool_paginator, })


def photo_filter_bnw(request):
    photo_post_bnw = Photo.objects.filter(category="흑백사진")
    photo_bnw_paginator = Paginator(photo_post_bnw, 4)
    photo_bnw_page = request.GET.get('page')
    photo_bnw_posts = photo_bnw_paginator.get_page(photo_bnw_page)

    return render(request, 'photo/photo_filter_bnw.html', {'photo_post_bnw': photo_post_bnw,
                                                           'photo_bnw_posts': photo_bnw_posts,
                                                           'photo_bnw_paginator': photo_bnw_paginator, })


def photo_filter_plus(request):
    photo_post_plus = Photo.objects.filter(category="플러스모델")
    photo_plus_paginator = Paginator(photo_post_plus, 4)
    photo_plus_page = request.GET.get('page')
    photo_plus_posts = photo_plus_paginator.get_page(photo_plus_page)

    return render(request, 'photo/photo_filter_plus.html', {'photo_post_plus': photo_post_plus,
                                                            'photo_plus_posts': photo_plus_posts,
                                                            'photo_plus_paginator': photo_plus_paginator, })



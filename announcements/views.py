# Create your views here.
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from announcements.forms import CommentForm
from announcements.models import Announcement, Comment


class AllAnnouncementsView(ListView):
    paginate_by = 3
    model = Announcement
    context_object_name = 'announcements'
    template_name = 'announcements/announcement_list.html'
    ordering = ['-created_at']


class AnnouncementDetailView(View):
    def get(self, request, pk):
        announcement = Announcement.objects.get(pk=pk)
        comments = Comment.objects.filter(post=announcement, reply=None)
        replies = Comment.objects.filter(post=announcement, reply__isnull=False)
        form = CommentForm()
        context = {'announcement': announcement,
                   'comments': comments,
                   'form': CommentForm()
                   }
        return render(request, 'announcements/announcement_detail.html', context)

    def post(self, request, pk):
        announcement = Announcement.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = announcement
            parent_id = request.POST.get('ParentId')
            if parent_id == "":
                form.save()
                messages.success(request, 'Comment posted successfully')
            else:
                form.instance.reply = Comment.objects.get(pk=parent_id)
                form.save()
                messages.success(request, 'Reply posted successfully')
        return redirect('announcements:announcement_detail', pk=pk)


class LikeAnnouncementView(View):
    def get(self, request, pk):
        return HttpResponseRedirect(reverse('announcements:announcement_detail', args=[pk]))

    def post(self, request, pk):
        post = get_object_or_404(Announcement, pk=pk)
        if request.user in post.liked.all():
            post.liked.remove(request.user)
        else:
            post.liked.add(request.user)

        announcement_list = request.POST.get('announcement_list')
        if announcement_list:
            return redirect('announcements:all_announcements')
        return HttpResponseRedirect(reverse('announcements:announcement_detail', args=[pk]))


class LikeCommentVIew(View):
    def get(self, request, pk):
        return HttpResponseRedirect(reverse('announcements:announcement_detail', args=[pk]))

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user in comment.liked.all():
            comment.liked.remove(request.user)
        else:
            comment.liked.add(request.user)
        return HttpResponseRedirect(reverse('announcements:announcement_detail', args=[comment.post.pk]))

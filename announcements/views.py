# Create your views here.
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView

from announcements.forms import CommentForm
from announcements.models import Announcement, Comment, AnnouncementSubscribers


class AnnouncementSubscriptionView(View):
    def get(self, request):
        # search email list for users email
        emails = AnnouncementSubscribers.objects.values_list('email', flat=True)
        user_email = request.user.email
        if user_email in emails:
            # delete user from email list
            AnnouncementSubscribers.objects.filter(email=user_email).delete()
        else:
            # add user to email list
            AnnouncementSubscribers.objects.create(email=user_email)
        return HttpResponseRedirect(reverse('announcements:all_announcements'))


class AllAnnouncementsView(ListView):
    paginate_by = 3
    model = Announcement
    context_object_name = 'announcements'
    template_name = 'announcements/announcement_list.html'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return super().get_context_data(**kwargs)

        context = super().get_context_data(**kwargs)
        context['subscribed'] = self.request.user.email in AnnouncementSubscribers.objects.values_list('email',
                                                                                                       flat=True)
        return context


class AnnouncementDetailView(View):
    def get(self, request, pk):
        announcement = Announcement.objects.get(pk=pk)
        comments = Comment.objects.filter(post=announcement, reply=None)
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


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'announcements/announcement_detail.html'
    context_object_name = 'comment'

    def get_success_url(self):
        messages.success(self.request, 'Comment deleted successfully')
        return reverse('announcements:announcement_detail', kwargs={'pk': self.object.post.id})


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


class SavedAnnouncementView(View):
    def get(self, request):
        saved_announcements = request.user.liked_announcements.all()
        paginator = Paginator(saved_announcements, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'announcements': page_obj,
            'page_obj': page_obj,
        }
        return render(request, 'announcements/saved_announcements.html', context)

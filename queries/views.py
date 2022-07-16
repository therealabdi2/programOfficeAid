from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from django.views.generic import ListView, DetailView, DeleteView

from queries.forms import QueryCommentForm
from queries.models import QueryPost, QueryComment


class DeleteQueryCommentView(DeleteView):
    model = QueryComment
    template_name = 'queries/query_detail.html'
    context_object_name = 'comment'

    def get_success_url(self):
        messages.success(self.request, 'Comment deleted successfully')
        return reverse('queryapp:query_detail', kwargs={'pk': self.object.post.id})


class LikeQueryCommentVIew(View):
    def get(self, request, pk):
        return HttpResponseRedirect(reverse('queryapp:query_detail', args=[pk]))

    def post(self, request, pk):
        comment = get_object_or_404(QueryComment, pk=pk)
        if request.user in comment.liked.all():
            comment.liked.remove(request.user)
        else:
            comment.liked.add(request.user)

        return redirect('queryapp:query_detail', comment.post.pk)


class QueryListView(ListView):
    paginate_by = 5
    model = QueryPost
    context_object_name = 'queries'
    template_name = 'queries/query_list.html'
    ordering = ['-created_at']


class QueryDetailView(View):
    def get(self, request, pk):
        query = QueryPost.objects.get(pk=pk)
        comments = QueryComment.objects.filter(post=query, reply=None)
        context = {'query': query,
                   'comments': comments,
                   'form': QueryCommentForm()
                   }
        return render(request, 'queries/query_detail.html', context)

    def post(self, request, pk):
        query_post = QueryPost.objects.get(pk=pk)
        form = QueryCommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = query_post
            parent_id = request.POST.get('ParentId')
            if parent_id == "":
                form.save()
                messages.success(request, 'Comment posted successfully')
            else:
                form.instance.reply = QueryComment.objects.get(pk=parent_id)
                form.save()
                messages.success(request, 'Reply posted successfully')
        return redirect('queryapp:query_detail', pk=pk)


class LikeQueryCommentView(View):
    def get(self, request, pk):
        return HttpResponseRedirect(reverse('queryapp:query_detail', args=[pk]))

    def post(self, request, pk):
        comment = QueryComment.objects.get(pk=pk)
        if request.user in comment.liked.all():
            comment.liked.remove(request.user)
        else:
            comment.liked.add(request.user)

        return redirect('queryapp:query_detail', comment.post.pk)


class LikeQueryView(View):
    def get(self, request, pk):
        return HttpResponseRedirect(reverse('queries:query_detail', args=[pk]))

    def post(self, request, pk):
        query = get_object_or_404(QueryPost, pk=pk)
        if request.user in query.liked.all():
            query.liked.remove(request.user)
        else:
            query.liked.add(request.user)

        query_list = request.POST.get('query_list')
        if query_list:
            return redirect('queryapp:query_list')

        return HttpResponseRedirect(reverse('queryapp:query_detail', args=[pk]))

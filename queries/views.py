from django.contrib import messages
from django.forms import forms
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.views import View

from django.views.generic import ListView, DetailView, DeleteView, CreateView

from queries.forms import QueryCommentForm
from queries.models import QueryPost, QueryComment


class UserQueryListView(ListView):
    model = QueryPost
    template_name = 'queries/query_list.html'
    context_object_name = 'queries'

    def get_queryset(self):
        return QueryPost.objects.filter(author=self.request.user)


class CreateQueryView(CreateView):
    model = QueryPost
    fields = ['title', 'body']
    template_name = 'queries/create_query.html'

    def get_success_url(self):
        return reverse('queryapp:query_detail', kwargs={'slug': self.object.slug})

    # check if slug already exists and throw error if it is
    def form_valid(self, form):
        if QueryPost.objects.filter(slug=form.instance.slug).exists():
            messages.error(self.request, 'Query with this title already exists')
            return HttpResponseRedirect(reverse('queryapp:make_query'))
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteQueryView(DeleteView):
    model = QueryPost
    template_name = 'queries/query_list.html'

    def get_success_url(self):
        return reverse('queryapp:query_list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise Http404
        return obj


class DeleteQueryCommentView(DeleteView):
    model = QueryComment
    template_name = 'queries/query_detail.html'
    context_object_name = 'comment'

    def get_success_url(self):
        messages.success(self.request, 'Comment deleted successfully')
        return reverse('queryapp:query_detail', kwargs={'slug': self.object.post.slug})


class LikeQueryCommentVIew(View):
    def get(self, request, pk):
        comment = get_object_or_404(QueryComment, pk=pk)
        return HttpResponseRedirect(reverse('queryapp:query_detail', args=[comment.post.slug]))

    def post(self, request, pk):
        comment = get_object_or_404(QueryComment, pk=pk)
        if request.user in comment.liked.all():
            comment.liked.remove(request.user)
        else:
            comment.liked.add(request.user)

        return HttpResponseRedirect(reverse('queryapp:query_detail', args=[comment.post.slug]))


class QueryListView(ListView):
    paginate_by = 5
    model = QueryPost
    context_object_name = 'queries'
    template_name = 'queries/query_list.html'
    ordering = ['-created_at']


class QueryDetailView(View):
    def get(self, request, slug):
        query = QueryPost.objects.get(slug=slug)
        comments = QueryComment.objects.filter(post=query, reply=None)
        context = {'query': query,
                   'comments': comments,
                   'form': QueryCommentForm()
                   }
        return render(request, 'queries/query_detail.html', context)

    def post(self, request, slug):
        query_post = QueryPost.objects.get(slug=slug)
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
        return redirect('queryapp:query_detail', slug=slug)


class LikeQueryCommentView(View):
    def get(self, request, pk):
        return HttpResponseRedirect(reverse('queryapp:query_detail', args=[pk]))

    def post(self, request, pk):
        comment = QueryComment.objects.get(pk=pk)
        print(comment)
        if request.user in comment.liked.all():
            comment.liked.remove(request.user)
        else:
            comment.liked.add(request.user)

        print(comment.post.slug)

        # redirect to query_detail page with slug of post
        return HttpResponseRedirect(reverse('queryapp:query_detail', args=[comment.post.slug]))


class LikeQueryView(View):
    def get(self, request, pk):
        return HttpResponseRedirect(reverse('queries:query_detail', args=[pk]))

    def post(self, request, slug):
        query = get_object_or_404(QueryPost, slug=slug)
        if request.user in query.liked.all():
            query.liked.remove(request.user)
        else:
            query.liked.add(request.user)

        query_list = request.POST.get('query_list')
        if query_list:
            return redirect('queryapp:query_list')

        return HttpResponseRedirect(reverse('queryapp:query_detail', args=[slug]))

from ajax_select import register, LookupChannel

from courses.models import Course


@register('courses')
class TagsLookup(LookupChannel):
    model = Course

    def check_auth(self, request):
        if request.user.full_name():
            return True

    def get_query(self, q, request):
        return self.model.objects.filter(course_name__icontains=q)

    def format_item_display(self, item):
        return u"<span class='course'>%s</span>" % item.course_name



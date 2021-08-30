from wagtail.core.models import Page
from wagtail_openedx.models import CourseIndexPage


class HomePage(Page):
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        course_index_page = self.get_children().type(CourseIndexPage).first()
        context["course_index_page"] = course_index_page
        context["courses"] = (
            course_index_page.get_children().live().order_by("-first_published_at")
        )
        return context

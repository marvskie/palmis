"""
Do not modify this file. It is generated from the Swagger specification.

Routing module.
"""
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
import exec.views as views

urlpatterns = [
    url(r"^upload$", views.Upload.as_view()),
    url(r"^task/(?P<branchId>.+)/(?P<dateString>.+)$", views.TaskBranchIdDateString.as_view()),
    url(r"^task/(?P<branchId>.+)$", views.TaskBranchId.as_view()),
    # url(r"^task$", views.Task.as_view()),
    url(r"^search$", views.Search.as_view()),
    url(r"^branch/category/files$", views.BranchCategoryFiles.as_view()),
    url(r"^branch/category/(?P<branchId>.+)$", views.BranchCategoryBranchId.as_view()),
    url(r"^branch$", views.Branch.as_view()),
    url(r"^file/comments/(?P<file_id>.+)$", views.get_comments),
    url(r"^file/comment$", views.add_comment),
    url(r"^task1/data$", views.get_tasks),
    url(r"^task1/crud$", views.add_task),
  
]

if settings.DEBUG:
    urlpatterns.extend([
        url(r"^the_specification/$", views.__SWAGGER_SPEC__.as_view()),
        url(r"^ui/(?P<path>.*)$", serve, {"document_root": "ui",
                                          "show_indexes": True})
    ])
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from app.views import QuestionList, ResponseDetail, QuestionDetail

urlpatterns = [
    path('openapi', get_schema_view(
        title="JustAskIt",
        description="API for the JustAskIt website",
        version="1.0.0",
    ), name='openapi-schema'),
    path("", TemplateView.as_view(template_name="swagger.html",
                                  extra_context={"schema_url": "openapi-schema"},
                                  ), name="swagger-ui"),
    path('questions', QuestionList.as_view(), name='questions'),
    path('questions/<int:pk>',
         csrf_exempt(QuestionDetail.as_view({'put': 'put', 'get': 'get', 'delete': 'delete'})),
         name='question detail'),
    path('responses/<int:pk>', csrf_exempt(ResponseDetail.as_view({'put': 'update_choices'})), name='response edit'),

]

"""opengrader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from opengrader_backend import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'examgroups', views.ExamGroupViewSet)
router.register(r'exams', views.GradedExamViewSet)
router.register(r'questions', views.QuestionExamViewSet)
router.register(r'keysheets', views.KeySheetViewSet)
router.register(r'keyquestions', views.KeyQuestionViewSet)
router.register(r'students', views.StudentViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    re_path('api/examdata/(?P<examgroup>.+)/$', views.ExamDataView.as_view()),
    re_path('api/preview/$', views.PreviewView.as_view()),
    re_path('api/chosendata/(?P<examgroup>.+)/$', views.ChosenDataView.as_view()),
    re_path('api/gradedata/(?P<examgroup>.+)/$', views.GradedDataView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # re_path(r'^upload/(?P<filename>[^/]+)$', views.ExamUploadView.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/upload/', views.FileUploadView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
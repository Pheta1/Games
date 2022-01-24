from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import StartBowlingView
from .views import UpdateBowlingScoreView
from .views import ScoreView

urlpatterns = [
    path(
        "",
        StartBowlingView.as_view(),
        name="start"
        ),
    path(
        'update/<int:pk>',
        UpdateBowlingScoreView.as_view(),
        name='udpate'
    ),
    path(
        'details/<int:pk>',
        ScoreView.as_view(),
        name='details'
    )
]
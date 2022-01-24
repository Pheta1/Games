from django import forms
from django.contrib.auth.models import User


class StartBowlingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StartBowlingForm, self).__init__(*args, **kwargs)
        self.fields['gamer'].choices = (
            (user.id, user.username)
            for user in User.objects.all().order_by('username')
        )
    lancer_score = forms.IntegerField(
        label='Nombre de quilles touchées'
    )
    gamer = forms.ChoiceField(
        label='Nom du joueur',
        required=True
    )


class UpdateBowlingScoreForm(forms.Form):
    def __init__(self, frame_number, lancer_number, gamer, *args, **kwargs):
        super(UpdateBowlingScoreForm, self).__init__(*args, **kwargs)
        self.fields["frame_number"].initial = frame_number
        self.fields["lancer_number"].initial = lancer_number
        self.fields["gamer"].initial = gamer

    frame_number = forms.IntegerField(
        required=False,
    )

    lancer_number = forms.IntegerField(
        required=False,
    )

    gamer = forms.CharField(
        required=False,
    )

    lancer_score = forms.IntegerField(
        label='Nombre de quilles touchées'
    )

# EOF

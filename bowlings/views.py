from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Lancer
from .models import Frame
from .models import Bowling
from .forms import StartBowlingForm
from .forms import UpdateBowlingScoreForm


class ScoreView(TemplateView):
    template_name = 'score.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bowling = Bowling.objects.get(pk=self.kwargs["pk"])

        frame_number = 1
        score_init = 0
        score = 0
        score_data = []
        score_list_data = []
        
        while frame_number <= 5:
            score_l, score = self.define_score(frame_number, score_init, bowling)
            if score == score_init:
                score_data.append("")
            else:
                score_data.append(score)
            for score_ in score_l:
                score_list_data.append(score_)
            score_init = score
            frame_number += 1

        context.update({
            'bowling': bowling,
            'score_data': score_data,
            'score_list_data': score_list_data,
            'score_actuel': score,
            'is_finished': bowling.is_finished
        })

        return context

    def define_score(self, frame_number, score_init, bowling):
        if frame_number == 5:
            score_l = ["" for i in range(6)]
        else:
            score_l = ["" for i in range(3)]
        score = score_init
        try:
            frame = Frame.objects.get(
                bowling=bowling,
                frame_number=frame_number
            )
            if frame.status == 'Simple':
                lancer_l = Lancer.objects.filter(frame=frame)
                index = 0
                for lancer in lancer_l:
                    score_l[index] = lancer.lancer_score
                    score += lancer.lancer_score
                    index += 1
            else:
                lancer = Lancer.objects.filter(
                    frame=frame,
                    is_additional=False
                ).last()
                score += 15
                if frame.status == 'Strike':
                    score_l[0] = "X"
                    bonus = 3
                else:
                    lancer_l = Lancer.objects.filter(
                        frame=frame,
                        is_additional=False
                    )
                    index = 0
                    for lancer_ in lancer_l:
                        if lancer_ == lancer:
                            score_l[index] = '/'
                        else:
                            score_l[index] = lancer.lancer_score
                        index += 1
                    bonus = 2

                id = lancer.id
                while bonus > 0:
                    try:
                        id += 1
                        lancer_b = Lancer.objects.get(id=id)
                        score += lancer_b.lancer_score
                        bonus -= 1
                    except Exception as e:
                        break

                    if frame.frame_number == 5:
                        lancer_additional = Lancer.objects.filter(
                            frame=frame,
                            is_additional=True
                        )
                        for lancer_add in lancer_additional:
                            index = lancer_add.lancer_number - 1
                            score_l[index] = lancer_add.lancer_score
        except Exception as e:
            pass

        return score_l, score


class StartBowlingView(FormView):
    form_class = StartBowlingForm
    template_name = 'start_bowling.html'

    def form_valid(self, form, *args, **kwargs):
        lancer_score = form.cleaned_data['lancer_score']
        gamer = User.objects.get(
            id=form.cleaned_data['gamer']
        )
        lancer_number = 1
        frame_number = 1

        if lancer_score == 15:
            status = 'Strike'
            is_done = True
        else:
            status = 'Simple'
            is_done = False

        bowling = Bowling.objects.create(
            gamer=gamer,
        )
        frame = Frame.objects.create(
            bowling=bowling,
            frame_number=frame_number,
            status=status,
            is_done=is_done
        )
        lancer = Lancer.objects.create(
            frame=frame,
            lancer_number=lancer_number,
            lancer_score=lancer_score
        )

        return HttpResponseRedirect(
            reverse('bowlings:details', args=(bowling.id,))
        )


class UpdateBowlingScoreView(FormView):
    form_class = UpdateBowlingScoreForm
    template_name = 'update_bowling.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bowling = Bowling.objects.get(pk=self.kwargs['pk'])
        last_frame = Frame.objects.filter(bowling=bowling).order_by('id').last()

        if last_frame.is_done:
            nombre_quilles = 15
        elif last_frame.frame_number == 5 and last_frame.status != "Simple":
            nombre_quilles = 15
        else:
            somme_lancer = 0
            for lancer in Lancer.objects.filter(frame=last_frame):
                somme_lancer += lancer.lancer_score
            nombre_quilles = 15 - somme_lancer
        context.update({
            'bowling': bowling,
            'nombre_quilles': nombre_quilles
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(UpdateBowlingScoreView, self).get_form_kwargs()
        bowling = Bowling.objects.get(pk=self.kwargs["pk"])
        last_frame = Frame.objects.filter(bowling=bowling).order_by('id').last()

        if last_frame.is_done:
            frame_number = last_frame.frame_number + 1
            lancer_number = 1
        else:
            frame_number = last_frame.frame_number
            last_lancer = Lancer.objects.filter(
                frame=last_frame
            ).order_by('id').last()
            lancer_number = last_lancer.lancer_number + 1

        kwargs['frame_number'] = frame_number
        kwargs['lancer_number'] = lancer_number
        kwargs['gamer'] = bowling.gamer.username

        return kwargs

    def form_valid(self, form, *args, **kwargs):
        lancer_score = form.cleaned_data['lancer_score']
        frame_number = form.cleaned_data['frame_number']
        lancer_number = form.cleaned_data['lancer_number']
        bowling = Bowling.objects.get(pk=self.kwargs["pk"])

        if lancer_number == 1:
            if lancer_score == 15:
                status = 'Strike'
                if frame_number == 5:
                    is_done = False
                else:
                    is_done = True
            else:
                status = 'Simple'
                is_done = False
            frame = Frame.objects.create(
                bowling=bowling,
                frame_number=frame_number,
                status=status,
                is_done=is_done
            )
            lancer = Lancer.objects.create(
                frame=frame,
                lancer_score=lancer_score,
                lancer_number=lancer_number
            )
            self.finished_bowling(bowling, frame)
        else:
            last_frame = Frame.objects.filter(
                bowling=bowling,
            ).last()
            lancer_l = Lancer.objects.filter(
                frame=last_frame,
                is_additional=False
            )
            is_additional = False
            somme_lancer = lancer_score
            for lancer in lancer_l:
                somme_lancer += lancer.lancer_score

            if last_frame.frame_number == 5 and last_frame.status != "Simple":
                lancer_supp = Lancer.objects.filter(
                    frame=last_frame,
                    is_additional=True
                )
                if last_frame.status == "Strike":
                    lancer_add = 3
                else:
                    lancer_add = 2
                if len(lancer_supp) + 1 < lancer_add:
                    is_done = False
                    status = last_frame.status
                    is_additional = True
                else:
                    is_done = True
                    status = last_frame.status
                    is_additional = True
            else:
                if somme_lancer == 15:
                    status = 'Spare'
                    if frame_number == 5:
                        is_done = False
                    else:
                        is_done = True
                else:
                    status = 'Simple'
                    if lancer_number == 3:
                        is_done = True
                    else:
                        is_done = False

            last_frame.status = status
            last_frame.is_done = is_done
            last_frame.save()

            new_lancer = Lancer.objects.create(
                frame=last_frame,
                lancer_number=lancer_number,
                lancer_score=lancer_score,
                is_additional=is_additional
            )
            self.finished_bowling(bowling, last_frame)

        return HttpResponseRedirect(
            reverse('bowlings:details', args=(bowling.id,))
        )

    def finished_bowling(self, bowling, frame):
        if frame.frame_number >= 5 and frame.is_done:
            bowling.is_finished = True
            bowling.save()
        else:
            bowling.is_finished = False
            bowling.save()




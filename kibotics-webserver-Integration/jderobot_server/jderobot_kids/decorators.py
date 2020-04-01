from django.core.exceptions import PermissionDenied
from jderobot_kids.models import Exercise, CodePermissions
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render, get_object_or_404

def error_handler404(request):
    return render(request,'jderobot_kids/error_page/404_error.html', {})

def user_have_exercise(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        exercise = get_object_or_404(Exercise, exercise_id=kwargs['exercise_id'])

        #user_exercises = [ex for pack in user.packs.all() for ex in pack.exercises.all()]
        #user_exercises += user.exercises.all()

        user_permissions = CodePermissions.objects.filter(Q(r=True)|Q(x=True)|Q(w=True), user=user)
        user_exercises = []
        for perm in user_permissions:
            user_exercises.append(perm.exercise)

        if exercise in user_exercises:
            return function(request, *args, **kwargs)
        else:
            return render(request,'jderobot_kids/error_page/404_error.html', {})
            #raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

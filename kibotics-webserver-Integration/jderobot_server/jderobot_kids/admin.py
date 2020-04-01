import string
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf.urls import url
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import djqscsv
from .models import User, CodePermissions, Host, Simulation, Exercise, Code
from taggit.models import Tag
from .forms import CodesGeneratorForm, IndividualPermissionsForm, GroupPermissionsForm, CodePacksForm, \
    GroupCreationForm, PackCreationForm
from django.db.models import Q


class MyAdminSite(AdminSite):
    """
        Overwrite admin default class (AdminSite) and extend it to allow personalised views
    """

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        urls += [
            url(r'codes_generator', self.admin_view(self.codes_generator)),
            url(r'group_permissions', self.admin_view(self.group_permissions)),
            url(r'individual_permissions', self.admin_view(self.individual_permissions)),
            url(r'group_creation', self.admin_view(self.create_group)),
            url(r'pack_creation', self.admin_view(self.create_pack))
        ]
        return urls

    def codes_generator(self, request):
        if request.method == 'GET':
            form = CodesGeneratorForm()
            return render(request, 'admin/codes_generator.html', {'form': form})
        else:
            form = CodesGeneratorForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                num_codes = int(form['num_codes'])
                for i in range(0, num_codes):
                    code_object = Code.objects.create(
                        code=self.code_generator(),
                        group=form["group"],
                        observations=form['observations'],
                        promotional=form['promotional'],
                        expires=form["expiration"]
                    )
                    code_object.packs.add(*form["packs"])
                    code_object.exercises.add(*form["exercises"])
            qs = Code.objects.all().order_by('-id')[:num_codes]
            return djqscsv.render_to_csv_response(qs)

    def code_generator(self, size=8, chars=string.ascii_letters + string.digits):
        """
            Generate random 8 digit codes with letters and numbers.
            If it generates an already created code, it generates a new one.
        """

        while True:
            code = ''.join(random.choice(chars) for _ in range(size))
            if not Code.objects.filter(code=code).exists():
                return code

    def individual_permissions(self, request):
        """
            Admin user permissions over a module (pack)
        """
        if request.method == 'GET':
            form = IndividualPermissionsForm()
            return render(request, 'admin/individual_permissions.html', {'form': form})
        else:
            form = IndividualPermissionsForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data

                usr = form["user"]
                for ex in form["exercises"]:
                    if CodePermissions.objects.filter(user=usr, exercise=ex).exists():
                        duplicated = CodePermissions.objects.filter(user=usr, exercise=ex)[0]
                        duplicated.delete()
                    CodePermissions.objects.create(
                        user=usr,
                        exercise=ex,
                        p=form["p"],
                        r=form["r"],
                        w=form["w"],
                        x=form["x"]
                    )
                for pack in form["packs"]:
                    pack_exercises = Exercise.objects.filter(tags=pack)
                    for ex in pack_exercises:
                        if CodePermissions.objects.filter(user=usr, exercise=ex).exists():
                            duplicated = CodePermissions.objects.filter(user=usr, exercise=ex)[0]
                            duplicated.delete()
                        CodePermissions.objects.create(
                            user=usr,
                            exercise=ex,
                            p=form["p"],
                            r=form["r"],
                            w=form["w"],
                            x=form["x"]
                        )
            else:
                print(form.errors)

            return HttpResponseRedirect("/admin/jderobot_kids/codepermissions/")

    def group_permissions(self, request):
        """
            Vista perteneciente al Admin que permite gestionar los permisos sobre un Ejercicio o Conjunto de Ejercicios para un Conjunto de Usuarios o Grupo
        """
        if request.method == 'GET':
            form = GroupPermissionsForm()
            return render(request, 'admin/group_permissions.html', {'form': form})
        else:
            form = GroupPermissionsForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                for u in User.objects.filter(group=form["group"]):
                    for ex in form["exercises"]:
                        if CodePermissions.objects.filter(user=u, exercise=ex).exists():
                            duplicated = CodePermissions.objects.filter(user=u, exercise=ex)[0]
                            duplicated.delete()
                        CodePermissions.objects.create(
                            user=u,
                            exercise=ex,
                            p=form["p"],
                            r=form["r"],
                            w=form["w"],
                            x=form["x"]
                        )
                    for pack in form["packs"]:
                        pack_exercises = Exercise.objects.filter(tags=pack)
                        for ex in pack_exercises:
                            if CodePermissions.objects.filter(user=u, exercise=ex).exists():
                                duplicated = CodePermissions.objects.filter(user=u, exercise=ex)[0]
                                duplicated.delete()
                        CodePermissions.objects.create(
                            user=u,
                            exercise=ex,
                            p=form["p"],
                            r=form["r"],
                            w=form["w"],
                            x=form["x"]
                        )

            return HttpResponseRedirect("/admin/jderobot_kids/codepermissions/")

    def create_group(self, request):
        """
            Create user groups using tags
        """
        if request.method == 'GET':
            form = GroupCreationForm()
            return render(request, 'admin/group_creation.html', {'form': form})
        else:
            form = GroupCreationForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                if not Tag.objects.filter(name=form["name"]).exists():
                    new_group = Tag.objects.create(name=form["name"])
                    new_group.save()
                for u in form["members"]:
                    u.group.add(form["name"])

                group_tag = Tag.objects.get(name=form["name"])
                return HttpResponseRedirect("/admin/jderobot_kids/user/?group__id__exact=" + str(group_tag.pk))
            else:
                return render(request, 'admin/group_creation.html', {'form': form})

    def create_pack(self, request):
        """
            Create new exercises pack assigning tags
        """
        if request.method == 'GET':
            form = PackCreationForm()
            return render(request, 'admin/pack_creation.html', {'form': form})
        else:
            form = PackCreationForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                if not Tag.objects.filter(name=form["name"]).exists():
                    new_pack = Tag.objects.create(name=form["name"])
                    new_pack.save()
                for e in form["exercises"]:
                    e.tags.add(form["name"])

                pack_tag = Tag.objects.get(name=form["name"])
                return HttpResponseRedirect("/admin/jderobot_kids/exercise/?pack=" + str(pack_tag.pk))
            else:
                return render(request, 'admin/pack_creation.html', {'form': form})


admin_site = MyAdminSite()


class UserPackListFilter(admin.SimpleListFilter):
    """ Custom Filter for Tags related to Packs in the User Model admin page """
    title = "Packs"
    parameter_name = 'pack'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        choices = []
        for pack in Exercise.tags.all():
            choices.append((pack.pk, pack.name))
        return choices

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            pack = Tag.objects.get(pk=self.value())
            exercises_of_pack = Exercise.objects.filter(tags=pack)
            users_with_pack_query = CodePermissions.objects.none()
            users_with_pack = None
            for exercise in exercises_of_pack:
                permissions_for_exercise = CodePermissions.objects.filter(Q(r=True) | Q(w=True) | Q(x=True),
                                                                          exercise=exercise)
                if not permissions_for_exercise:
                    # if no permissions found for any exercise of the pack, exit (nobody has the pack)
                    users_with_pack = []
                    break
                users_with_exercise = []
                for permission in permissions_for_exercise:
                    users_with_exercise.append(permission.user)  # get users with permissions over the exercise
                if not users_with_pack:
                    users_with_pack = users_with_exercise
                else:
                    users_with_pack = [value for value in users_with_exercise if
                                       value in users_with_pack]  # intersection

            for user in users_with_pack:
                # convert users_with_pack to <Queryset> object to return
                users_with_pack_query = users_with_pack_query | User.objects.filter(username=user.username)

            if not users_with_pack_query:
                return queryset.none()
            else:
                return users_with_pack_query
        else:
            return queryset


class CustomUserAdmin(UserAdmin):
    filter_horizontal = ('user_permissions', 'groups',
                         'code')  # ManyToMany Fields displayed as two selectable tables    #'packs', 'exercises',
    list_filter = (
    'role', UserPackListFilter, ('group', admin.RelatedOnlyFieldListFilter), 'is_staff', 'is_superuser', 'is_active')
    list_display = ['username', 'first_name', 'last_name', 'role', 'Code', 'Group', 'email', 'last_login',
                    'date_joined']
    ordering = ['username']

    # Structure #('group_tittle', {'fields' : ('field1','field2',)}),
    # inlines = [UsersGroupInline] # Display the UsersGroup of the User
    fieldsets = (
        ('User Credentials', {'fields': ('username', 'password',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('JdeRobotKids Info', {'fields': ('role', 'code', 'group', 'observations', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)}),
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'subscription_expiration',)}))

    change_list_template = "admin/group_creation_button.html"

    def Code(self, obj):
        return "\n".join([p.code for p in obj.code.all()])

    def Group(self, obj):
        return "\n".join([p.name for p in obj.group.all()])


admin.site.register(User, CustomUserAdmin)


class CodePermissionsAdmin(admin.ModelAdmin):
    list_filter = ('exercise', 'user',)
    list_display = ['id', 'user', 'exercise', 'p', 'r', 'w', 'x']
    change_list_template = "admin/manage_group_permissions_button.html"


admin.site.register(CodePermissions, CodePermissionsAdmin)


class HostAdmin(admin.ModelAdmin):
    list_display = ['host', 'active', 'ip', 'main_server']


admin.site.register(Host, HostAdmin)


class SimulationAdmin(admin.ModelAdmin):
    list_display = ['init_simulation', 'minutes_up', 'active', 'user', 'simulation_type', 'client_ip', 'host_ip']

    order = ['-init_simulation']

    def minutes_up(self, obj):
        return str(obj.up_time()) + ' minutes'


admin.site.register(Simulation, SimulationAdmin)


class ExercisePackListFilter(admin.SimpleListFilter):
    """ Custom Filter for Tags related to Packs in the Exercise Model admin page """
    title = "Packs"
    parameter_name = 'pack'

    def lookups(self, request, model_admin):
        choices = []
        for pack in Exercise.tags.all():
            choices.append((pack.pk, pack.name))
        return choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__pk=self.value())
        else:
            return queryset


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'state', 'compute_load', 'observations']
    list_filter = (ExercisePackListFilter,)

    change_list_template = "admin/pack_creation_button.html"


admin.site.register(Exercise, ExerciseAdmin)


class CodePackListFilter(admin.SimpleListFilter):
    """ Custom Filter for Tags related to Packs in the Code Model admin page """
    title = "Packs"
    parameter_name = 'pack'

    def lookups(self, request, model_admin):
        choices = []
        for pack in Exercise.tags.all():
            choices.append((pack.pk, pack.name))
        return choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(packs__pk=self.value())
        else:
            return queryset


class CodeAdmin(admin.ModelAdmin):
    filter_horizontal = ('packs',)
    list_filter = ('group', CodePackListFilter,)
    list_display = ['id', 'code', 'group', 'observations', 'expires']
    change_list_template = "admin/codes_geneator_button.html"

    form = CodePacksForm


admin.site.register(Code, CodeAdmin)

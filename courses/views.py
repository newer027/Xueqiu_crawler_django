# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.forms.models import modelform_factory
from django.db.models import Count
from django.apps import apps
from django.core.cache import cache
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, \
                         CsrfExemptMixin, JsonRequestResponseMixin
from students.forms import CourseEnrollForm
from .models import Subject, Course, Module, Content
from .forms import ModuleFormSet


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset() #super, get_queryset的用法
        return qs.filter(owner=self.request.user) #filter的用法


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user #.instance.owner的用法
        return super(OwnerEditMixin, self).form_valid(form) #form_valid的用法


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin): #OwnerMixin的用法
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin): #OwnerEditMixin的用法
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list') #reverse_lazy的用法
    template_name = 'courses/manage/course/form.html' #template_name的用法


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data) #ModuleFormSet的用法

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk) #dispatch的用法

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset}) #render_to_response的用法

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset}) #render_to_response的用法


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name) #get_model的用法
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model,
                                 exclude=['owner', 'order', 'created', 'updated']) #modelform_factory的用法
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super(ContentCreateUpdateView,
                     self).dispatch(request, module_id, model_name, id) #dispatch的用法

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj) #get_form的用法
        return self.render_to_response({'form': form,
                                        'object': self.obj}) #render_to_response的用法

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # 新的content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id) #redirect的用法

        return self.render_to_response({'form': form,
                                        'object': self.obj}) #render_to_response的用法


class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id) #redirect的用法


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'module': module}) #render_to_response的用法


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                                  course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'}) #render_json_response的用法


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request):
        for id, order in self.request_json.items(): #request_json的用法
            Content.objects.filter(id=id,
                                   module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'}) #render_json_response的用法


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = cache.get('all_subjects') #cache.get的用法
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects) #cache.set的用法
        all_courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = 'subject_{}_courses'.format(subject.id)
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses}) #render_to_response的用法


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs) #get_context_data的用法
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object}) #CourseEnrollForm,initial的用法
        return context

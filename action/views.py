from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from action.forms import TreatmentForm, TreatmentFilterForm, TreatmentAppendForm, ConsultingFilterForm, \
    ConsultingForm, TreatmentProcessForm
from action.models import Treatment, TreatmentProcess, Consulting, TreatmentProcessImages


# Create your views here.

def consulting_overview(request):
    mobile = request.GET.get('mobile')
    consultings = Consulting.objects.all()
    if mobile:
        consultings = consultings.filter(customer__mobile__icontains=mobile)
    context = {
        'consult_total': Consulting.objects.all().count(),
        'consult_lookup': consultings.count(),
        'form': ConsultingFilterForm(),
        'consultings': consultings.order_by('-id')
    }
    return render(request, 'action/consultant/overview.html', context)


"""
class Consulting_All(LoginRequiredMixin, ListView):
  template_name = 'action/consultant/overview.html'
  login_url = 'manager:login'
  model = get_user_model()
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['consultings'] = Consulting.objects.order_by('-id')
    return context
"""


class ConsultingNew(LoginRequiredMixin, CreateView):
    model = Consulting
    form_class = ConsultingForm
    template_name = 'action/consultant/create.html'
    login_url = 'manager:login'
    success_url = reverse_lazy('action:consultant_overview')


class ConsultingView(LoginRequiredMixin, DetailView):
    queryset = Consulting.objects.select_related('consultor')
    template_name = 'action/consultant/single.html'
    context_object_name = 'consulting'
    login_url = 'manager:login'


class ConsultingUpdate(LoginRequiredMixin, UpdateView):
    model = Consulting
    form_class = ConsultingForm
    template_name = 'action/consultant/edit.html'
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('action:consultant_view', kwargs={'pk': self.kwargs['pk']})


def treatment_overview(request):
    mobile = request.GET.get('mobile')
    treatments = Treatment.objects.all()
    if mobile:
        treatments = treatments.filter(customer__mobile__icontains=mobile)
    context = {
        'treat_total': Treatment.objects.all().count(),
        'treat_lookup': treatments.count(),
        'form': TreatmentFilterForm(),
        'treatments': treatments.order_by('-id')
    }
    return render(request, 'action/treatment/overview.html', context)


class TreatmentAll(LoginRequiredMixin, ListView):
    template_name = 'action/treatment/overview.html'
    login_url = 'manager:login'
    model = get_user_model()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['treatments'] = Treatment.objects.order_by('-id')
        return context


class TreatmentNew(LoginRequiredMixin, CreateView):
    model = Treatment
    form_class = TreatmentForm
    template_name = 'action/treatment/create.html'
    login_url = 'manager:login'
    success_url = reverse_lazy('action:treatment_overview')


class TreatmentView(LoginRequiredMixin, DetailView):
    queryset = Treatment.objects.select_related('customer')
    template_name = 'action/treatment/single.html'
    context_object_name = 'treatment'
    login_url = 'manager:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            query = TreatmentProcess.objects.filter(tag=self.object.pk).order_by('date')
            context["treat_pros"] = query
            query_img = TreatmentProcessImages.objects.filter(treat=self.object.pk)
            context["treat_pro_images"] = query_img
            return context
        except ObjectDoesNotExist:
            return context


class TreatmentAppend(LoginRequiredMixin, FormMixin, ListView):
    model = TreatmentProcess
    template_name = 'action/treatment/append.html'
    form_class = TreatmentAppendForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('action:treatment_view', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.form_class
        form = self.get_form()
        if form.is_valid():
            TreatmentProcess.objects.create(
                tag=self.kwargs['pk'],
                date=form.cleaned_data['date'],
                status=form.cleaned_data['status']
            )
            TreatmentProcessImages.objects.create(
                treat=self.kwargs['pk'],
                treat_pro=TreatmentProcess.objects.all().count(),
                thumb=form.cleaned_data['thumb']
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message # passed in form.cleaned_data['message']
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        if 'pk' in self.kwargs:
            context['treatment'] = Treatment.objects.get(pk=self.kwargs['pk'])
            context['treat_pros'] = TreatmentProcess.objects.filter(tag=self.kwargs['pk']).order_by('date')
            return context
        else:
            return context


class TreatmentUpdate(LoginRequiredMixin, UpdateView):
    model = Treatment
    template_name = 'action/treatment/edit.html'
    form_class = TreatmentForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('action:treatment_view', kwargs={'pk': self.kwargs['pk']})

    # success_url = reverse_lazy('action:treatment_overview')


class TreatmentDelete(LoginRequiredMixin, DeleteView):
    pass


class TreatmentProcessUpdate(LoginRequiredMixin, UpdateView):
    model = TreatmentProcess
    template_name = 'action/treatmentpro/edit.html'
    form_class = TreatmentProcessForm
    login_url = 'manager:login'

    # success_url = reverse_lazy('action:treatment_overview')

    def get_context_data(self):
        context = super().get_context_data()
        query = TreatmentProcess.objects.get(pk=self.kwargs['pk'])
        context['treat_pro'] = query
        context['treat'] = Treatment.objects.get(id=str(query.tag))
        context['treat_pro_images'] = TreatmentProcessImages.objects.filter(treat_pro=query.id)
        return context

    def get_success_url(self):
        treat_pro = TreatmentProcess.objects.get(pk=self.kwargs['pk'])
        treat = Treatment.objects.get(id=str(treat_pro.tag))

        if (treat_pro.tmp_thumb != "") and (treat_pro.tmp_thumb is not None):
            TreatmentProcessImages.objects.create(
                treat=treat_pro.tag,
                treat_pro=treat_pro.id,
                thumb=treat_pro.tmp_thumb
            )
            TreatmentProcess.objects.filter(tag=treat_pro.tag).update(
                tmp_thumb=None
            )

        return reverse('action:treatment_view', kwargs={'pk': treat.pk})


def treatment_process_update_delete(request, pk, img_tag):
    img = TreatmentProcessImages.objects.get(id=img_tag)
    img.delete()

    return redirect('action:treatmentpro_update', pk)

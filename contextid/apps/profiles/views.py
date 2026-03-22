from django.db import transaction
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import *
from .forms import *
from apps.attributes.forms import AttributeFormSet

# ---------------------- Detail --------------------------------------------
class IdentityProfileDetail(LoginRequiredMixin, DetailView):
    model = IdentityProfile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_queryset(self):
        # Security: User A cannot see User B's profile details by typing the ID in the URL
        return IdentityProfile.objects.filter(
            user=self.request.user
            ).select_related('context').prefetch_related('attributes__value_type')

# ---------------------- Create --------------------------------------------
class IdentityProfileCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = IdentityProfile
    form_class = IdentityProfileForm
    template_name = 'profiles/profile_create.html'
    success_message = "Identity Profile created successfully."

    def get_form_kwargs(self):
        """Pass the current user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['attributes'] = AttributeFormSet(self.request.POST)
        else:
            data['attributes'] = AttributeFormSet()
        return data

    def form_valid(self, form):
        context_data = self.get_context_data()
        attributes = context_data['attributes']
        
        # Use a transaction so we don't save a profile if attributes fail
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            if attributes.is_valid():
                attributes.instance = self.object
                attributes.save()
                return super().form_valid(form)
            else:
                # If attributes are invalid, we need to roll back and show errors
                return self.render_to_response(self.get_context_data(form=form))
            
    def get_success_url(self):
        return reverse_lazy('profiles:profile_detail', kwargs={'pk': self.object.pk})

# ---------------------- Update --------------------------------------------
class IdentityProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = IdentityProfile
    form_class = IdentityProfileForm 
    context_object_name = 'profile'
    template_name_suffix = '_update_form'
    success_message = "Identity Profile updated successfully."
    
    def get_queryset(self):
        return IdentityProfile.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            # Load formset with POST data and the existing profile instance
            data['attributes'] = AttributeFormSet(self.request.POST, instance=self.object)
        else:
            # Load formset with existing data from the database
            data['attributes'] = AttributeFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        attributes = context['attributes']

        # --- Handle (existing) Profile Picture Removal ---
        # Check if the hidden 'clear_image' flag was set to 'true' by our JavaScript
        if self.request.POST.get('clear_image') == 'true':
            # Delete the physical file from storage (Render/Local)
            if form.instance.profile_pic:
                try:
                    form.instance.profile_pic.delete(save=False)
                except Exception:
                    pass
            
            # Set the database field to None
            form.instance.profile_pic = None
        
        # Save the main profile form
        self.object = form.save()

        # Save the formset (handles updates, deletions, and new additions)
        if attributes.is_valid():
            attributes.instance = self.object
            attributes.save()
            return super().form_valid(form)
        else:
            # Re-render with errors if formset is invalid
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('profiles:profile_detail', kwargs={'pk': self.object.pk})
            
# ---------------------- Delete --------------------------------------------
class IdentityProfileDelete(LoginRequiredMixin, DeleteView):
    model = IdentityProfile
    success_url = reverse_lazy('accounts:dashboard')

    def get_queryset(self):
        # Security: User A cannot delete User B's profile
        return IdentityProfile.objects.filter(user=self.request.user)
    
    # DeleteView requires a manual message because it doesn't use form_valid
    def post(self, request, *args, **kwargs):
        messages.success(request, "Identity Profile deleted successfully.")
        return super().delete(request, *args, **kwargs)
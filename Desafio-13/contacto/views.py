from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import ContactoForm
from django.urls import reverse_lazy
from django.contrib import messages

class ContactoUsuario(CreateView):
		template_name = 'contacto/contacto.html'
		form_class = ContactoForm
		success_url = reverse_lazy('apps.contacto:contacto')

		def get_context_data(self, **kwargs):
			context = super().get_context_data(**kwargs)
			context['request'] = self.request
			return context
		
		def form_valid(self, form):
			messages.success(self.request, 'Consulta enviada')
			return super().form_valid(form)

# def contacto(request):
# 	data = {'form': ContactoForm()}
	
# 	if request.method == 'POST':
# 		formulario = ContactoForm(data = request.POST)
# 		if formulario.is_valid():
# 			formulario.save()
# 			data['mensaje'] = 'Mensaje enviado'
# 		else:
# 			data['form'] = formulario
# 	return render(request, 'contacto/contacto.html', data)
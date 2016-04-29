from django.contrib import messages
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import VariationInventoryFormSet
from .models import Product, Variation



class VariationListView(ListView):
	model = Variation
	queryset = Variation.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(VariationListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		print "formset:::"
		print context["formset"]
		return context

	def get_queryset(self, *args, **kwargs):
		print "*****get_queryset*****"
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			print "product:::"
			print product
			queryset = Variation.objects.filter(product=product)
			print "qs:::"
			print queryset
		return queryset

	def post(self, request, *args, **kwargs):
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		print request.POST 
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				form.save()
				messages.success(request, "Your inventory and pricing has been updated.")
				return redirect("products")
		raise Http404



class ProductListView(ListView):
	model = Product
	queryset = Product.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data()
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q")
		return context

	def get_queryset(self, *args, **kwargs):
		print "^^^^^"
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			print "*****"
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			try:
				qs = self.model.objects.filter(
				Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass

		return qs

class ProductDetailView(DetailView):
	model = Product






# def product_detail_view_func(request, id):
# 	# product_instance = Product.objects.get(id=id)
# 	product_instance = get_object_or_404(Product, id=id)

# 	template = "products/product_detail.html"
# 	context = {
# 		"object": product_instance
# 	}
# 	return render(request, template, context)

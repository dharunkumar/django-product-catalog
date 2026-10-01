from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Tag


class ProductListFilterTests(TestCase):
	def setUp(self):
		self.electronics = Category.objects.create(name='Test Electronics')
		self.clothing = Category.objects.create(name='Test Clothing')
		self.featured = Tag.objects.create(name='Test Featured')
		self.sale = Tag.objects.create(name='Test Sale')
		self.other_tag = Tag.objects.create(name='Test Other')

	def create_product(self, name, description, category, tags=()):
		product = Product.objects.create(
			name=name,
			description=description,
			price='19.99',
			category=category,
		)
		product.tags.add(*tags)
		return product

	def test_combines_description_category_and_tag_filters(self):
		matching_product = self.create_product(
			'Matching product',
			'needle wireless headphones',
			self.electronics,
			(self.featured, self.sale),
		)
		self.create_product(
			'Wrong category',
			'needle wireless clothing',
			self.clothing,
			(self.featured,),
		)
		self.create_product(
			'Wrong description',
			'a wired audio product',
			self.electronics,
			(self.featured,),
		)
		self.create_product(
			'Wrong tag',
			'needle wireless speaker',
			self.electronics,
			(self.other_tag,),
		)

		response = self.client.get(
			reverse('product_list'),
			{
				'q': 'needle',
				'category': self.electronics.name,
				'tags': [self.featured.name, self.sale.name],
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context['products']), [matching_product])

	def test_empty_result_set_renders_gracefully(self):
		response = self.client.get(
			reverse('product_list'),
			{'q': 'no-product-has-this-description'},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['products'].count(), 0)
		self.assertContains(response, 'No products found matching the specified criteria.')

	def test_multiple_matching_tags_do_not_duplicate_products(self):
		product_with_both_tags = self.create_product(
			'Two matching tags',
			'a product with both test tags',
			self.electronics,
			(self.featured, self.sale),
		)
		product_with_one_tag = self.create_product(
			'One matching tag',
			'a product with one test tag',
			self.clothing,
			(self.featured,),
		)

		response = self.client.get(
			reverse('product_list'),
			{'tags': [self.featured.name, self.sale.name]},
		)

		products = list(response.context['products'])
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(products), 2)
		self.assertCountEqual(
			products,
			[product_with_both_tags, product_with_one_tag],
		)

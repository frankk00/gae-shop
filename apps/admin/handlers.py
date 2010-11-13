# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Administration Application Handlers

"""
from tipfy import RequestHandler, Response, cached_property, redirect
from tipfy.ext.jinja2 import render_response
from tipfy.ext.i18n import gettext as _

from forms import BlogPostForm, ProductForm

from apps.blog.models import BlogPost
from apps.shop.models import Product


class AdminIndexHandler(RequestHandler):
    """Main view for Admin"""
    def get(self, **kwargs):
        context = {}
        return render_response('admin/index.html', **context)


class ShopIndexHandler(RequestHandler):
    def get(self, **kwargs):
        products = Product.all().order('-modified')
        result = products.fetch(10)
        context = {
            'products': result,
        }
        return render_response('admin/shop/index.html', **context)


class ProductsIndexHandler(RequestHandler):
    def get(self, **kwargs):
        products = Product.all().order('-modified')
        result = products.fetch(10)
        context = {
            'products': result,
        }
        return render_response('admin/product/index.html', **context)


class ProductHandler(RequestHandler):
    def get(self, product_id=None, **kwargs):
        """Return a product to edit or an empty form to create"""
        template = 'admin/product/new.html'
        context = {
            'form': self.form,
        }
        # render edit form
        if product_id is not None:
            product = Product.get_by_id(product_id)
            if product:
                self.form = ProductForm(obj=product)
                self.form.tags.data = ', '.join(product.tags)
                context.update({ 'form': self.form })
                template = 'admin/product/edit.html'
            else:
                return redirect('/admin/shop/')
        # render new form
        return render_response(template, **context)
    
    def post(self, product_id=None, **kwargs):
        """Handle submitted form data"""
        # validate form
        if self.form.validate():
            name = self.form.name.data
            description = self.form.description.data
            price = self.form.price.data
            unit = self.form.unit.data
            live = self.form.live.data
            tags = self.form.tags.data
            if tags is not None:
                tags = [tag.strip() for tag in tags.split(',') if tag != '']
            # save edit form
            if product_id:
                product = Product.get_by_id(product_id)
                product.name = name
                product.description = description
                product.price = price
                product.unit = unit
                product.live = live
                product.tags = tags
            # save new form
            else:
                product = Product(name=name, description=description, price=price, unit=unit, live=live, tags=tags)
            if product.put():
                return redirect('admin/shop')
        return self.get(**kwargs)
        
    @cached_property
    def form(self):
        """Form instance as cached_property"""
        return ProductForm(self.request)


class BlogIndexHandler(RequestHandler):
    """Return date ordered blog posts"""
    def get(self, **kwargs):
        posts = BlogPost.all().order('-modified')
        result = posts.fetch(10)
        context = {
            'posts': result,
        }
        return render_response('admin/blog/index.html', **context)


class BlogPostHandler(RequestHandler):
    """Manage individual blog posts"""
    def get(self, post_id=None, **kwargs):
        """Return a post to edit or an empty form to create"""
        template = 'admin/blog/new.html'
        context = {
            'form': self.form,
        }
        # render edit
        if post_id is not None:
            post = BlogPost.get_by_id(post_id)
            if post:
                self.form = BlogPostForm(obj=post)
                self.form.tags.data = ', '.join(post.tags)
                context.update({ 'form': self.form })
                template = 'admin/blog/edit.html'
            else:
                return redirect('admin/blog/')
        # render new
        return render_response(template, **context)
    
    def post(self, post_id=None, **kwargs):
        """Handle submitted form data"""
        # validate form
        if self.form.validate():
            title = self.form.title.data
            lead = self.form.lead.data
            content = self.form.content.data
            live = self.form.live.data
            tags = self.form.tags.data
            print content
            if tags is not None:
                tags = [tag.strip() for tag in tags.split(',') if tag != '']
            # saving edited
            if post_id:
                post = BlogPost.get_by_id(post_id)
                post.title = title
                post.lead = lead
                post.content = content
                post.live = live
                post.tags = tags
            # creating new
            else:
                post = BlogPost(title=title, lead=lead, content=content, live=live, tags=tags)
            if post.put():
                return redirect('admin/blog')
        return self.get(**kwargs)
    
    @cached_property
    def form(self):
        """Form instance as cached_property"""
        return BlogPostForm(self.request)


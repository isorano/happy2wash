from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db
from .models import Customer, Gender, JobType, JobStatus, Job, OrderStatus, Order
from flask_appbuilder.actions import action
from flask import redirect
from datetime import datetime
from flask_appbuilder.api import BaseApi, expose, rison

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""
from flask_appbuilder.widgets import ShowWidget


class MyShowWidget(ShowWidget):
     template = 'widgets/myshow.html'
"""
    Filler functions
"""
def fill_gender():
	try:
		db.session.add(Gender(name="Unknown"))
		db.session.add(Gender(name="Male"))
		db.session.add(Gender(name="Female"))
		db.session.commit()
	except Exception:
		db.session.rollback()

def fill_job_status():
	try:
		num_rows_deleted = db.session.query(JobStatus).delete()
		db.session.commit()
	except:
		db.session.rollback()
	try:
		db.session.add(JobStatus(name="CheckIn"))
		db.session.add(JobStatus(name="Processed"))
		db.session.add(JobStatus(name="Finished"))
		db.session.add(JobStatus(name="CheckOut"))
		db.session.commit()
	except Exception:
		db.session.rollback()
	
def fill_job_type():
	try:
		num_rows_deleted = db.session.query(JobType).delete()
		db.session.commit()
	except:
		db.session.rollback()
	try:
		db.session.add(JobType(name="Cuci Kering Lipat 3 Kg", price=24000, discount=0))
		db.session.add(JobType(name="Cuci Kering Lipat 6 Kg", price=28500, discount=20))
		db.session.add(JobType(name="Cuci Kering Lipat 10 Kg", price=47000, discount=20))
		db.session.add(JobType(name="Cuci Kering Lipat > 10Kg per-Kg", price=8000, discount=20))
		db.session.add(JobType(name="Cuci Kering Lipat 6 Jam per-Kg", price=24000, discount=0))
		db.session.add(JobType(name="Cuci Kering Setrika 3 Kg", price=28500, discount=0))
		db.session.add(JobType(name="Cuci Kering Setrika 6 Kg", price=38500, discount=20))
		db.session.add(JobType(name="Cuci Kering Setrika 10 Kg", price=64000, discount=20))
		db.session.add(JobType(name="Cuci Kering Setrika > 10Kg per-Kg", price=9500, discount=20))
		db.session.add(JobType(name="Cuci Kering Setrika 6 Jam per-Kg", price=20000, discount=0))
		db.session.add(JobType(name="Setrika 3 Kg", price=20000, discount=0))
		db.session.add(JobType(name="Setrika 6 Kg", price=35000, discount=0))
		db.session.add(JobType(name="Setrika > 6Kg per-Kg", price=7000, discount=0))
		db.session.add(JobType(name="Cuci Bed Cover Size Single (satuan)", price=25000, discount=0))
		db.session.add(JobType(name="Cuci Bed Cover Size Queen-King (satuan)", price=35000, discount=0))
		db.session.add(JobType(name="Cuci Bed Cover Size Super-King (satuan)", price=40000, discount=0))
		db.session.commit()
	except Exception:
		db.session.rollback()

def fill_order_status():
	try:
		num_rows_deleted = db.session.query(OrderStatus).delete()
		db.session.commit()
	except:
		db.session.rollback()
	try:
		db.session.add(OrderStatus(name="Received"))
		db.session.add(OrderStatus(name="Finished"))
		db.session.add(OrderStatus(name="Paid"))
		db.session.commit()
	except Exception:
		db.session.rollback()

def clear_jobs():
	try:
		num_rows_deleted = db.session.query(Job).delete()
		db.session.commit()
	except:
		db.session.rollback()
		
def clear_orders():
	try:
		num_rows_deleted = db.session.query(Order).delete()
		db.session.commit()
	except:
		db.session.rollback()

"""
    ModelViews
"""
class JobModelView(ModelView):
	datamodel = SQLAInterface(Job)
	
	label_columns = {'name':'Job','cidate':'Checkin', 'codate':'Checkout', 'weight':'Qty', 'job_type':'Product', 'job_status':'Status'}
	list_columns = ["job_type", "weight", "price", "job_status", "order"]
	base_order = ("cidate", "asc")
	show_columns = ["name", "cidate", "codate", "job_type", "weight", "price", "job_status"]
	add_columns = ["order", "job_type", "weight"]
	edit_columns = ["cidate", "codate",  "job_type", "weight", "job_status"]
	
	def pre_add(self, item):
		add_order = db.session.get(Order, item.order.id)
		otype = db.session.get(JobType, item.job_type.id)
		item.cidate = add_order.cidate
		item.price = item.weight * otype.price * ((100 - otype.discount)/100.0)
		#item.name = add_order.name + "-" + str(item.id)
		
	def post_add(self, item):
		add_order = db.session.get(Order, item.order.id)
		add_order_name = add_order.name
		add_job = db.session.get(Job, item.id)
		item.name = add_order_name + "-" + str(item.id)
		db.session.commit()

	def pre_update(self, item):
		otype = db.session.get(JobType, item.job_type.id)
		item.price = item.weight * otype.price * ((100 - otype.discount)/100.0)

class OrderModelView(ModelView):
	datamodel = SQLAInterface(Order)
	#show_template = 'show_orders.html'
	show_widget = MyShowWidget
	
	label_columns = {'order.name':'Order','cidate':'Received', 'codate':'Finished', 
		'customer.name': 'Name', 'customer.phone': 'Phone', 'customer.address':'Address', 'order_status':'Status'}
	list_columns = ["name", "cidate", "order_status", "customer"]
	base_order = ("cidate", "desc")
	show_fieldsets = [
		("Summary", {"fields": ["id", "cidate", "codate", "order_status", "deposit", "price"]}),
		("Customer", {"fields": ["customer.name", "customer.phone", "customer.address"], "expanded": True}),
	]
	add_columns = ["cidate", "customer", "deposit", "order_status"]
	edit_columns = ["cidate", "codate", "order_status", "deposit", "price"]
	
	related_views = [JobModelView]
	
	#edit_template = 'appbuilder/general/model/edit_cascade.html'
	#show_template = 'appbuilder/general/model/show_cascade.html'
	
	@action("myaction","Calculate Total Price","Are you sure?","fa-rocket")
	def myaction(self, item):
		"""
    		do something with the item record
		"""
		order_price = 0
		my_jobs = db.session.query(Job).filter(Job.order_id == item.id).all()
		for job in my_jobs: 
			print("XXXXX", job.id)	
			order_price += job.price
		#item.price = order_price
		my_order = db.session.get(Order, item.id)
		my_order.price = order_price
		db.session.commit()
		self.update_redirect() # update redirect stack
		return redirect(self.get_redirect())

	def post_add(self, item):
		add_order = db.session.get(Order, item.id)
		item.name = str(item.id) + "-" + item.cidate.strftime('%m%d%Y')
		db.session.commit()

	def pre_update(self, item):
		if (item.codate != None):
			print("XXXXX")
			my_jobs = db.session.query(Job).filter(Job.order_id == item.id).all()
			for job in my_jobs: 
				print("YYYYY", job.id)
				if (job.codate == None):
					print("ZZZZZ")
					job.codate = item.codate
			db.session.commit()
		if (item.order_status.id == 2): # Finished, ready for payment/pickup/delivery
			print("AAAAA")
			item.codate = datetime.now()
			my_jobs = db.session.query(Job).filter(Job.order_id == item.id).all()
			for job in my_jobs: 
				print("BBBBB", job.id)
				job.job_status_id = 3 # Finished
			db.session.commit()

class CustomerModelView(ModelView):
	datamodel = SQLAInterface(Customer)
	
	list_columns = ["name", "phone", "email"]
	base_order = ("name", "asc")
	show_fieldsets = [
		("Summary", {"fields": ["name", "phone", "address"]}),
		("Detail", {"fields": ["email", "birthday", "gender"], "expanded": True}),
	]
	
	add_columns = ["name", "phone", "address", "email", "birthday", "gender"]
	
	edit_columns = ["name", "phone", "address", "email", "birthday", "gender"]
	
	related_views = [OrderModelView]
	
	show_template = 'appbuilder/general/model/show_cascade.html'

class JobTypeModelView(ModelView):
	datamodel = SQLAInterface(JobType)
	
	list_columns = ["id", "name", "price", "discount"]

"""
    API test
"""
class ExampleApi(BaseApi):
	route_base = '/myapi/v1'
	# http://localhost:5000/myapi/v1/greeting
	
	@expose('/greeting')
	@rison()
	def greeting(self, **kwargs):
		if 'order' in kwargs['rison']:
			order_id = kwargs['rison']['order']
			my_order = db.session.get(Order, order_id)
			order_text = "<html><head><title>Order details</title></head><body>"
			if (my_order == None):
				return self.response_400(message="order not found")
			order_text = "<h2>Order:" + my_order.name + "</h2><p>Date received: " + my_order.cidate.strftime("%m/%d/%Y") + "</p><p>Total: " +\
				str(my_order.price) + "</p><p>Deposit: " + str(my_order.deposit) + "</p><p>" + "To be paid: " + str(my_order.price - my_order.deposit) + "</p><hr>" +\
				"<table><tr><td>Job#</td><td>Name</td><td>Qty</td><td>Unit Price</td><td>Discount</td><td>Total</td><td>Final Price</td></tr>"
			my_jobs = db.session.query(Job).filter(Job.order_id == my_order.id).all()
			for job in my_jobs:
				job_type = db.session.get(JobType, job.job_type.id)
				order_text = order_text	+ "<tr><td>" + str(job.id) + "</td><td>" + job_type.name +\
					"</td><td>" + str(job.weight) + "</td><td>" + str(job_type.price) +\
					"</td><td>" + str(job_type.discount) + "%</td><td>" + str(job.weight *  job_type.price) + "</td><td>" + str(job.price) + "</td></tr>"

#			return self.response(
#				200,
#				message = order_text
#			)
			return(order_text + "</table></body></html>")
		return self.response_400(message="order not found")

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
	return (
		render_template(
			"404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
		),
		404,
	)
	
"""
    Housekeeping
"""
db.create_all()
fill_gender()
fill_job_status()
fill_job_type()
fill_order_status()

#clear_jobs()
#clear_orders()

appbuilder.add_view(
	JobTypeModelView,
	"List Products",
	#icon="fa-user",
	#category="Customers",
)

appbuilder.add_view(
	CustomerModelView,
	"List Customers",
	#icon="fa-user",
	#category="Customers",
)

appbuilder.add_view(
	OrderModelView,
	"List Orders",
	#icon="fa-user",
	#category="Orders",
)

appbuilder.add_view(
	JobModelView,
	"List Jobs",
	#icon="fa-user",
	#category="Orders",
)

appbuilder.add_api(ExampleApi)

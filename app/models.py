from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who

"""
class OrderStatus(Model):
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	
	def __repr__(self):
		return self.name

class JobStatus(Model):
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	
	def __repr__(self):
		return self.name

class JobType(Model):
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	price = Column(Integer, nullable=False)
	discount = Column(Integer, nullable=True, default=0)
	
	def __repr__(self):
		return self.name

class Gender(Model):
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	
	def __repr__(self):
		return self.name
	
class Customer(Model):
	id = Column(Integer, primary_key=True)
	name = Column(String(100), unique=True, nullable=False)
	address = Column(String(200), nullable=False)
	birthday = Column(Date, nullable=True)
	email = Column(String(50))
	phone = Column(String(20), nullable=False)
	gender_id = Column(Integer, ForeignKey("gender.id"))
	gender = relationship("Gender")
	
	def __repr__(self):
		return self.name

class Order(Model):
	id = Column(Integer, primary_key=True)
	name = Column(String(100), unique=True, nullable=True)
	cidate = Column(Date, nullable=False)
	codate = Column(Date, nullable=True)
	deposit = Column(Integer, nullable=True, default=0)
	price = Column(Integer, nullable=True, default=0)
	payment = Column(Integer, nullable=True)
	order_status_id = Column(Integer, ForeignKey("order_status.id"), nullable=False)
	order_status = relationship("OrderStatus")
	customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
	customer = relationship("Customer")
	
	def __repr__(self):
		return self.name
		# if using DateTime: %m%d%Y%H%M

class Job(Model):
	id = Column(Integer, primary_key=True)
	name = Column(String(100), unique=True, nullable=True)
	weight = Column(Integer, nullable=False)
	cidate = Column(Date, nullable=False)
	codate = Column(Date, nullable=True)
	price = Column(Integer, nullable=True)
	job_type_id = Column(Integer, ForeignKey("job_type.id"), nullable=False, default=1)
	job_type = relationship("JobType")
	job_status_id = Column(Integer, ForeignKey("job_status.id"), nullable=False, default=1)
	job_status = relationship("JobStatus")
	order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
	order = relationship("Order")
	
	def __repr__(self):
		return self.name


"""
end end end
"""

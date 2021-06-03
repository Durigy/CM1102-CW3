from datetime import datetime, timedelta, date, time
from shop import db, login_manager
from flask_login import UserMixin

# Used for help: https://stackoverflow.com/questions/52133438/sqlalchemy-default-datetime-now-plus-n-days-from-now/52134177
# This function creates a date 1 day from the current date/time
# def generate_date():
#     date = datetime.utcnow() + timedelta(days=1)
#     return date


# # ----- Pop Tracker Stuff ----- #
# class PopTracker(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True) # Must be randomly generated
#     # name = db.Column(db.String(50), unique=True, nullable=False)
    
#     # Links 
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     pop_tracker_type_id = db.Column(db.Integer, db.ForeignKey('pop_tracker_type.id'), nullable=False)

#     # Relationships 
#     pop_tracker_item = db.relationship('Pop_Tracker_Item', backref='pop_tracker', lazy=True)

#     # def __repr__(self):
#     #     return f"Post('{self.date}', '{self.content}')" # edit


# class PopTrackerItem(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True) # Must be randomly generated
#     date_add = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
#     # Links 
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     pop_tracker_id = db.Column(db.Integer, db.ForeignKey('pop_tracker.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.date_add}')" # edit ?


# class PopTrackerType(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True)
#     tracker_type_name = db.Column(db.String(50), unique=True, nullable=False)

#     # Relationships 
#     pop_tracker = db.relationship('Pop_Tracker', backref='pop_tracker_type', lazy=True)

#     def __repr__(self):
#         return f"Post('{self.tracker_type_name}')" # edit ?


# ----- Wish List Stuff ----- #
# class WishList(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key=True) # Must be randomly generated
#     wish_list_name = db.Column(db.String(100), nullable=False, default="My Wish List")
#     date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     # Links 
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
#     wish_list_privacy_id = db.Column(db.Integer, db.ForeignKey('wish_list_privacy.id'), nullable=False, default=1)
#     # wish_list_purpose_id = db.Column(db.Integer, db.ForeignKey('wish_list_purpose.id'), nullable=False)

#     # Relationships 
#     wish_list_item = db.relationship('WishListItem', backref='wish_list', lazy=True)

#     def __repr__(self):
#         return f"Post('{self.wish_list_name}', '{self.date_created}')" # edit ?


class WishListItem(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True) # Must be randomly generated
    date_add = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # importance_number = db.Column(db.Integer, nullable=True)
    
    # Links
    product_id = db.Column(db.String(20), db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)

    # wish_list_id = db.Column(db.String(20), db.ForeignKey('wish_list.id'), nullable=False)
    # wish_list_purpose_id = db.Column(db.Integer, db.ForeignKey('wish_list_purpose.id'), nullable=False, default=1)
    # purchased_id = db.Column(db.Integer, db.ForeignKey('purchased.id'), nullable=False)

    # # Relationships 
    # purchased_item = db.relationship('PurchasedItem', backref='wish_list_item', lazy=True)

    def __repr__(self):
        return f"Post('{self.date_add}')" # edit ?


# class WishListPrivacy(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True)
#     privacy_setting = db.Column(db.String(50), unique=True, nullable=False)

#     # Relationships 
#     wish_list = db.relationship('WishList', backref='wish_list_privacy', lazy=True)

#     def __repr__(self):
#         return f"Post('{self.privacy_setting}')" # edit ?


# class WishListPurpose(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True)
#     purpose_name = db.Column(db.String(50), unique=True, nullable=False)

#     # Relationships 
#     wish_list = db.relationship('Wish_List', backref='wish_list_purpose', lazy=True)

#     def __repr__(self):
#         return f"Post('{self.purpose_name}')" # edit ?


# ----- Order Stuff ----- #
class Order(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True) # Must be randomly generated
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address_first_line = db.Column(db.String(120), nullable=True)
    address_second_line = db.Column(db.String(120), nullable=True)
    address_city = db.Column(db.String(120), nullable=True)
    address_country = db.Column(db.String(120), nullable=True)
    address_postcode = db.Column(db.String(10), nullable=True)
    # order_number = db.Column(db.Integer, unique=True, nullable=False)
    product_count = db.Column(db.Integer, nullable=False)
    date_ordered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_discount = db.Column(db.Integer, nullable=False)
    order_total = db.Column(db.Integer, nullable=False)
    shipped_date = db.Column(db.DateTime, nullable=True)

    # Links 
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    # cupon_id = db.Column(db.Integer, db.ForeignKey('cupon.id'), nullable=True)
    shipped_status_id = db.Column(db.Integer, db.ForeignKey('shipped_status.id'), nullable=False, default=1)

    # Relationships 
    purchased_item = db.relationship('PurchasedItem', backref='order', lazy=True)

    def __repr__(self):
        return f"Post('{self.order_number}', '{self.product_count}', '{self.date_ordered}', '{self.order_discount}', '{self.order_total}', '{self.shipped_date}')" # edit ?


class PurchasedItem(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True) # Must be randomly generated
    product_count = db.Column(db.Integer, nullable=False)
    total_purchase_amount = db.Column(db.Integer, nullable=False)
    is_returned = db.Column(db.Boolean, nullable=False, default=False)
    returned_date = db.Column(db.DateTime, nullable=True)
    
    # Links 
    order_id = db.Column(db.String(20), db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.String(20), db.ForeignKey('product.id'), nullable=False)
    # wish_list_item_id = db.Column(db.Integer, db.ForeignKey('Wish_List_Item.id'), nullable=True)

    # Relationships 
    # rating = db.relationship('Rating', backref='purchased_item', lazy=True)
    # wish_list_item = db.relationship('Wish_List_Item', backref='purchased', lazy=True)

    def __repr__(self):
        return f"Post('{self.product_count}', '{self.total_purchase_amount}', '{self.is_returned}', '{self.returned_date}')" # edit ?


# class Cupon(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True) # Must be randomly generated 
#     cupon_code = db.Column(db.String(100), unique=True, nullable=False)
#     date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     discount = db.Column(db.Integer, nullable=False)
#     expiration_date = db.Column(db.DateTime, nullable=False, default=generate_date())
#     uses_per_user = db.Column(db.Integer, nullable=False, default=1)
#     stock = db.Column(db.Integer, nullable=False, default=1)

#     # Relationships 
#     order = db.relationship('Order', backref='cupon', lazy=True)
    
#     def __repr__(self):
#         return f"Post('{self.cupon_code}', '{self.date_created}', '{self.discount}', '{self.expiration_date}', '{self.uses_per_user}', '{self.stock}')" # edit ?


class ShippedStatus(db.Model):
    # Datebase Columns 
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), unique=True, nullable=False)
    
    # Relationships 
    order = db.relationship('Order', backref='shipped_status', lazy=True)

    def __repr__(self):
        return f"Post('{self.status}')" # edit ?


# ----- Product Stuff ----- #
class Product(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True) # Must be randomly generated
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False, default=10.00)
    discount_amount = db.Column(db.Integer, nullable=False, default=0)
    date_listed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stock = db.Column(db.Integer, nullable=False, default=1)
    pop_number = db.Column(db.Integer, nullable=False, default=0)
    feature_image = db.Column(db.String(20), nullable=False, default='default_product_pic')
    prduct_image_1 = db.Column(db.String(20), nullable=True)               
    prduct_image_2 = db.Column(db.String(20), nullable=True)               
    prduct_image_3 = db.Column(db.String(20), nullable=True)               
    prduct_image_4 = db.Column(db.String(20), nullable=True)               
    prduct_image_5 = db.Column(db.String(20), nullable=True)
    short_description = db.Column(db.Text, nullable=False)
    long_description = db.Column(db.Text, nullable=True)
    vaulted = db.Column(db.Boolean, nullable=False, default=False)
    is_draft = db.Column(db.Boolean, nullable=False, default=True)
    
    # Links 
    pop_category_id = db.Column(db.Integer, db.ForeignKey('pop_category.id'), nullable=False)
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchise.id'), nullable=False)
#     charater_name_id = db.Column(db.Integer, db.ForeignKey('charater_name.id'), nullable=False)
    # pop_number_id = db.Column(db.Integer, db.ForeignKey('pop_number.id'), nullable=False)
    pop_box_size_id = db.Column(db.Integer, db.ForeignKey('pop_box_size.id'), nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)

    # Relationships 
    rating = db.relationship('Rating', backref='product', lazy=True)
    wish_list_item = db.relationship('WishListItem', backref='product', lazy=True)
#     pop_tracker = db.relationship('Pop_Tracker', backref='product', lazy=True)
#     purchased_item = db.relationship('PurchasedItem', backref='product', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.short_description}', '{self.long_description}', '{self.price}', '{self.discount_amount}', '{self.date_listed}', '{self.stock}', '{self.feature_image}', '{self.prduct_image_1}', '{self.prduct_image_2}', '{self.prduct_image_3}', '{self.prduct_image_4}', '{self.prduct_image_5}', '{self.vaulted}')" # edit ?


class PopCategory(db.Model):
    # Datebase Columns 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    
    # Relationships 
    products = db.relationship('Product', backref='pop_category', lazy=True)

    def __repr__(self):
        return f"{self.name}" # edit ?


class Franchise(db.Model):
    # Datebase Columns 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    
    # Relationships 
    product = db.relationship('Product', backref='franchise', lazy=True)

    def __repr__(self):
        return f"{self.name}" # edit ?


# class CharaterName(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)
    
#     # Relationships 
#     product = db.relationship('Product', backref='charater_name', lazy=True)

#     def __repr__(self):
#         return f"Post('{self.franchise_name}')" # edit ?


# class PopNumber(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.Integer, unique=True, nullable=False)
    
#     # Relationships 
#     product = db.relationship('Product', backref='pop_number', lazy=True)

#     def __repr__(self):
#         return f"Post('{self.franchise_name}')" # edit ?


class PopBoxSize(db.Model):
    # Datebase Columns 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    depth = db.Column(db.Integer, nullable=False)

    # Relationships 
    product = db.relationship('Product', backref='pop_box_size', lazy=True)

    def __repr__(self):
        return f"{self.name}, {self.width}, {self.height}, {self.depth}" # edit ?


class Rating(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True) # Must be randomly generated
    rating_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=True)
    
    # Links 
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    parent_rating_id = db.Column(db.String(20), db.ForeignKey('rating.id'), nullable=True)
    # purchased_item_id = db.Column(db.String(20), db.ForeignKey('purchased_item.id'), nullable=True)
    product_id = db.Column(db.String(20), db.ForeignKey('product.id'), nullable=False)

    # Relationships
    parent_rating = db.relationship('Rating', backref='rating', remote_side=id, lazy=True)

    def __repr__(self):
        return f"Rating('{self.rating_number}', '{self.title}', '{self.content}')" # edit ?

        
# ----- User Stuff ----- #
class User(UserMixin, db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key=True) # Must be randomly generated
    username = db.Column(db.String(15), unique=True, nullable=False)
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.Text, nullable=True)
    address_postcode = db.Column(db.String(10), nullable=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile_pic')
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    
#     # Links 
#     user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)

    # Relationships 
#     # pop_tracker = db.relationship('Pop_Tracker', backref='user', lazy=True)
    # wish_list = db.relationship('WishList', backref='user', lazy=True)
    order = db.relationship('Order', backref='user', lazy=True)
    rating = db.relationship('Rating', backref='user', lazy=True)
    product = db.relationship('Product', backref='user', lazy=True)
    wish_list_item = db.relationship('WishListItem', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.profile_image}', '{self.firstname}', '{self.lastname}', '{self.email}', '{self.address}', '{self.address_postcode}')" # edit ?


# class UserRole(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True)
#     role = db.Column(db.String(15), unique=True, nullable=False)

#     # Relationships 
#     user = db.relationship('User', backref='user_role', lazy=True)

#     def __repr__(self):
#         return f"User Role('{self.role}')" # edit ?


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



# class Comment(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
    
#     # Links 
#     parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
#     # Relationships 
#     # parent = db.relationship('Comment', backref='comment_parent', remote_side=id, lazy=True)

#     def __repr__(self):
#         return f"comment('{self.date}', '{self.content}')" # edit

# class Post(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
    
#     # Links 
#     comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
#     # Relationships

#     def __repr__(self):
#         return f"Post('{self.date}', '{self.content}')" # edit

import secrets
import os
from PIL import Image
from flask import render_template, url_for, request, redirect, flash, session, abort
from shop import app, db, bcrypt
from shop.models import Franchise, Order, PopBoxSize, PopCategory, Product, User, WishListItem
from shop.forms import LoginForm, RegistrationForm, UpdateAccountForm, CreateProductForm, AddFranchiseForm, AddBoxSizeForm, AddCategoryForm, UpdateCartForm, OrderForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
def index():
    products = Product.query.filter(db.and_(Product.stock > 0, Product.is_draft == 0)).order_by(Product.date_listed).all()
    filter_by='date_listed'
    form = UpdateCartForm()

    return render_template(
        'index.html',
        title='Home',
        products=products,
        heading='Newest',
        form=form
    )

@app.route("/title")
def filter_title():
    products = Product.query.filter(db.and_(Product.stock > 0, Product.is_draft == 0)).order_by(Product.title).all()

    form = UpdateCartForm()
    return render_template(
        'index.html',
        title='Filted By Title',
        products=products,
        heading='Title A-Z',
        form=form
    )

@app.route("/price")
def filter_price():
    products = Product.query.filter(db.and_(Product.stock > 0, Product.is_draft == 0)).order_by(Product.price).all()
   
    form = UpdateCartForm()
    return render_template(
        'index.html',
        title='Filted By Price',
        products=products,
        heading='Price',
        form=form
    )

@app.route("/<string:filter_type>/<string:name>")
def filter_by(filter_type, name):
    if filter_type == 'category':        
        products = Product.query.join(PopCategory).filter(db.and_(Product.stock > 0, Product.is_draft == 0, PopCategory.name.lower() == name.lower() )).all()
    
    elif filter_type == 'franchise':
        products = Product.query.join(Franchise).filter(db.and_(Product.stock > 0, Product.is_draft == 0, Franchise.name.lower() == name.lower() )).all()


    form = UpdateCartForm()

    return render_template(
        'index.html',
        title='Filted By ' + name,
        heading=name,
        products=products,
        form=form
    )

#when '/home' or '/index' are type or redirected to it will the redirect to the url without anything after the /
@app.route("/index")
@app.route("/home")
def home():
    return redirect(url_for('index'))


#################################
#                               #
#           User Stuff          #
#                               #
#################################

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = secrets.token_hex(10)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            id=user_id, 
            username=form.username.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()
        flash('Account Created - Login in')
        return redirect(url_for('login'))
    return render_template(
        'user/register.html',
        title='Register',
        form=form
    )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash('Login Unsuccessful. Check Email and Password')
    
    return render_template(
        'user/login.html',
        title='Login',
        form=form
    )

@app.route("/logout")
def logout():
    logout_user()
    clear_cart()
    return redirect(request.referrer)

def save_account_pic(form_picture):
    random_hex = secrets.token_hex(10)
    pic_file_name = random_hex + '.jpg'
    picture_path = os.path.join(app.root_path, 'static/img/profile', pic_file_name)

    output_size = (125, 125)
    processed_image = Image.open(form_picture)
    processed_image.thumbnail(output_size)
    processed_image.save(picture_path)

    return random_hex

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            form_picture = save_account_pic(form.picture.data)
            current_user.profile_image = form_picture

        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.address_postcode = form.address_postcode.data
        db.session.commit()
        flash('Your account was updated')

        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.address_postcode.data = current_user.address_postcode
    
    profile_image = url_for('static', filename='img/profile/' + current_user.profile_image + '.jpg')
    
    wish_list = []
    wish_items = WishListItem.query.filter(WishListItem.user_id == current_user.id).all()
    # products = Product.query.join(WishListItem).filter(WishListItem == wish_items).all()
    products = db.session.query(WishListItem, Product).filter(WishListItem.user_id == current_user.id).all()
    for i in wish_items:
        prod = Product.query.filter(Product.id == i.product_id).first()
        # print(prod.id)
        wish_list.append(prod)
    form2 = UpdateCartForm()
    print(wish_list)
    return render_template(
        'user/account.html',
        title='Account',
        profile_image=profile_image,
        form=form,
        products=wish_list,
        form2=form2
    )

# Reference: https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', title='Page Not Found'), 404


def save_product_pic(form_picture):
    random_hex = secrets.token_hex(10)
    pic_file_name = random_hex + '.jpg'
    picture_path = os.path.join(app.root_path, 'static/img/products', pic_file_name)

    output_size = (400, 400)
    processed_image = Image.open(form_picture)
    processed_image.thumbnail(output_size)
    processed_image.save(picture_path)

    return random_hex


#################################
#                               #
#         Product Stuff         #
#                               #
#################################

@app.route("/product/<string:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    products = Product.query.join(PopCategory).filter(db.and_(Product.stock > 0, Product.is_draft == 0, PopCategory.id == product.pop_category.id, Product.id != product.id )).limit(5)
    
    if (current_user.is_authenticated == False) and ((product.is_draft == True)):
        abort(404)
    elif current_user.is_authenticated == True:
        if (current_user.is_admin == False) and ((product.is_draft == True)):
                abort(404)

    final_price = (100 - product.discount_amount) /100
    final_price = product.price * final_price

    form = UpdateCartForm()

    return render_template(
        'products/product.html',
        title=product.title,
        product=product,
        products=products,
        final_price=final_price,
        form=form
    )


#################################
#                               #
#          Admin Stuff          #
#                               #
#################################


@app.route("/admin/product/new", methods=['GET', 'POST'])
@login_required
def create_product():
    # if current_user.is_admin != 1:
    #     abort(404)
        # flash("Sorry you need to be an admin to access that page")
        # return redirect(url_for('index'))

    # product = Product.query.all()
    pop_categorys = PopCategory.query.all()
    franchises = Franchise.query.all()
    pop_box_sizes = PopBoxSize.query.all()
    form = CreateProductForm()
    if form.validate_on_submit():

        feature_image = None
        prduct_image_1 = ''
        prduct_image_2 = ''
        prduct_image_3 = ''
        prduct_image_4 = ''
        prduct_image_5 = ''

        if form.feature_image.data:
            form_picture = save_product_pic(form.feature_image.data)
            feature_image = form_picture
        
        if form.prduct_image_1.data:
            form_picture = save_product_pic(form.prduct_image_1.data)
            prduct_image_1 = form_picture
        
        if form.prduct_image_2.data:
            form_picture = save_product_pic(form.prduct_image_2.data)
            prduct_image_2 = form_picture
        
        if form.prduct_image_3.data:
            form_picture = save_product_pic(form.prduct_image_3.data)
            prduct_image_3 = form_picture
        
        if form.prduct_image_4.data:
            form_picture = save_product_pic(form.prduct_image_4.data)
            prduct_image_4 = form_picture
        
        if form.prduct_image_5.data:
            form_picture = save_product_pic(form.prduct_image_5.data)
            prduct_image_5 = form_picture
        
        product_id = secrets.token_hex(10)

        product = Product(
            id = product_id,
            title=form.title.data,
            price=form.price.data,
            discount_amount=form.discount_amount.data,
            stock=form.stock.data,
            feature_image=feature_image,
            prduct_image_1=prduct_image_1,
            prduct_image_2=prduct_image_2,
            prduct_image_3=prduct_image_3,
            prduct_image_4=prduct_image_4,
            prduct_image_5=prduct_image_5,
            short_description=form.short_description.data,
            long_description=form.long_description.data,
            vaulted=form.vaulted.data,
            is_draft=form.is_draft.data,
            pop_category_id=request.form.get('category'),
            franchise_id=request.form.get('franchise'),
            pop_box_size_id=request.form.get('pop_box_size'),
            user=current_user
        )
        db.session.add(product)
        db.session.commit()
        flash('The product was created')
        return redirect(url_for('admin_all_products'))
    return render_template(
        'products/create_product.html',
        title='New Product',
        form=form,
        legend='Create a New Product',
        pop_categorys=pop_categorys,
        franchises=franchises,
        pop_box_sizes=pop_box_sizes
    )


@app.route("/product/<string:product_id>/update", methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user != current_user:
        abort(403)

    pop_categorys = PopCategory.query.all()
    franchises = Franchise.query.all()
    pop_box_sizes = PopBoxSize.query.all()

    prduct_image_1 = product.prduct_image_1
    prduct_image_2 = product.prduct_image_2
    prduct_image_3 = product.prduct_image_3
    prduct_image_4 = product.prduct_image_4
    prduct_image_5 = product.prduct_image_5

    product.prduct_image_1 = prduct_image_1
    product.prduct_image_2 = prduct_image_2
    product.prduct_image_3 = prduct_image_3
    product.prduct_image_4 = prduct_image_4
    product.prduct_image_5 = prduct_image_5
    form = CreateProductForm()

    if form.validate_on_submit():
        if form.feature_image.data:
            form_picture = save_product_pic(form.feature_image.data)
            feature_image = form_picture
            product.feature_image = feature_image
        

        if form.prduct_image_1.data:
            form_picture = save_product_pic(form.prduct_image_1.data)
            product.prduct_image_1 = form_picture
        print(form.remove_prduct_image_1.data)
        if form.remove_prduct_image_1.data:
            product.prduct_image_1 = ''

        if form.prduct_image_2.data:
            form_picture = save_product_pic(form.prduct_image_2.data)
            product.prduct_image_2 = form_picture
        if form.remove_prduct_image_2.data:
            product.prduct_image_2 = ''

        if form.prduct_image_3.data:
            form_picture = save_product_pic(form.prduct_image_3.data)
            product.prduct_image_3 = form_picture
        if form.remove_prduct_image_3.data:
            product.prduct_image_3 = ''

        if form.prduct_image_4.data:
            form_picture = save_product_pic(form.prduct_image_4.data)
            product.prduct_image_4 = form_picture
        if form.remove_prduct_image_4.data:
            product.prduct_image_4 = ''

        if form.prduct_image_5.data:
            form_picture = save_product_pic(form.prduct_image_5.data)
            product.prduct_image_5 = form_picture
        if form.remove_prduct_image_5.data:
            product.prduct_image_5 = ''

        product.title = form.title.data
        product.price = form.price.data
        product.discount_amount = form.discount_amount.data
        product.stock = form.stock.data
        product.pop_number = form.pop_number.data
        product.short_description = form.short_description.data
        product.long_description = form.long_description.data
        product.vaulted = form.vaulted.data
        product.is_draft = form.is_draft.data
        
        product.pop_category_id=request.form.get('category'),
        product.franchise_id=request.form.get('franchise'),
        product.pop_box_size_id=request.form.get('pop_box_size'),


        db.session.commit()

        flash('The product was updated')
        
        return redirect(url_for('product', product_id=product.id))
    elif request.method == 'GET':
        # Pre input form with values from the database
        form.title.data = product.title
        form.price.data = product.price
        form.discount_amount.data = product.discount_amount
        form.stock.data = product.stock
        form.pop_number.data = product.pop_number
        form.short_description.data = product.short_description
        form.long_description.data = product.long_description
        form.vaulted.data = product.vaulted
        form.is_draft.data = product.is_draft

    return render_template(
        'products/update_product.html',
        title="Update Product",
        form=form,
        legend='Update Product',
        pop_categorys=pop_categorys,
        franchises=franchises,
        pop_box_sizes=pop_box_sizes,
        pop_category_preset=product.pop_category_id,
        franchise_preset=product.franchise_id,
        pop_box_size_preset=product.pop_box_size_id,
        product=product
    )


@app.route("/admin") #,  methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_admin != 1:
        abort(404)
    products = Product.query.all()
    stock = Product.query.filter(((Product.stock > 0) & (Product.is_draft == 0))).count()
    stock_out = Product.query.filter(((Product.stock == 0) )).count()
    draft = Product.query.filter(Product.is_draft > 0).count()
    return render_template(
        'admin/admin_home.html',
        title="Admin Area",
        products=products,
        stock=stock,
        draft=draft,
        stock_out=stock_out
    )

@app.route("/admin/products") #,  methods=['GET', 'POST'])
@login_required
def admin_all_products():
    if current_user.is_admin != 1:
        abort(404)
    # products = Product.query.all()
    products = Product.query.filter(((Product.stock >= 3) & (Product.is_draft == 0)))
    return render_template(
        'admin/products_a_a.html',
        title="All Products - Admin Area",
        items='Products',
        products=products
    )

@app.route("/admin/products/drafts") #,  methods=['GET', 'POST'])
@login_required
def admin_all_draft_products():
    if current_user.is_admin != 1:
        abort(404)
    products = Product.query.filter(Product.is_draft == 1)
    return render_template(
        'admin/products_a_a.html',
        title="Draft Products - Admin Area",
        items='Draft Products',
        products=products
    )

@app.route("/admin/products/low_stock") #,  methods=['GET', 'POST'])
@login_required
def admin_all_low_stock_products():
    if current_user.is_admin != 1:
        abort(404)
    products = Product.query.filter(((Product.stock < 3) & (Product.is_draft == 0)))
    return render_template(
        'admin/products_a_a.html',
        title="Low Stock - Admin Area",
        items='Products Low in Stock',
        products=products
    )

@app.route("/admin/categories", methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.is_admin != 1:
        abort(404)
        # flash("Sorry you need to be an admin to access that page")
        # return redirect(url_for('index'))

    pop_categorys = PopCategory.query.all()

    form = AddCategoryForm()
    if form.validate_on_submit():
        category_id = secrets.token_hex(5)

        category = PopCategory(
            name=form.name.data
        )
        db.session.add(category)
        db.session.commit()
        flash('The Category was created')
        return redirect(url_for('add_category'))
    return render_template(
        'admin/add_category.html',
        title='New Category',
        form=form,
        legend='Create a New Category',
        items='Categories',
        list_display=pop_categorys
    )

@app.route("/admin/franchises", methods=['GET', 'POST'])
@login_required
def add_franchise():
    if current_user.is_admin != 1:
        abort(404)
        # flash("Sorry you need to be an admin to access that page")
        # return redirect(url_for('index'))
    
    franchises = Franchise.query.all()

    form = AddFranchiseForm()
    if form.validate_on_submit():
        category_id = secrets.token_hex(5)

        category = Franchise(
            name=form.name.data
        )
        db.session.add(category)
        db.session.commit()
        flash('The Franchise was created')
        return redirect(url_for('add_franchise'))
    return render_template(
        'admin/add_franchise.html',
        title='New Franchise',
        form=form,
        legend='Create a New Franchise',
        items='Franchises',
        list_display=franchises
    )

@app.route("/admin/box_sizes", methods=['GET', 'POST'])
@login_required
def add_box_size():
    if current_user.is_admin != 1:
        abort(404)
        # flash("Sorry you need to be an admin to access that page")
        # return redirect(url_for('index'))

    pop_box_sizes = PopBoxSize.query.all()

    form = AddBoxSizeForm()
    if form.validate_on_submit():
        category_id = secrets.token_hex(5)

        box_size = PopBoxSize(
            name=form.name.data,
            width=form.width.data,
            height=form.height.data,
            depth=form.depth.data
        )
        db.session.add(box_size)
        db.session.commit()
        flash('The Box size was created')
        return redirect(url_for('add_box_size'))
    return render_template(
        'admin/add_box_sizes.html',
        title='New Box Size',
        form=form,
        legend='Create a New Box Size',
        items='Box Sizes',
        list_display=pop_box_sizes
    )

#################################
#                               #
#           Cart Stuff          #
#                               #
#################################

@app.route("/add_to_cart", methods=['GET', 'POST'])
def add_to_cart():
    if 'basket' not in session:
        session['basket'] = [{'total_quant': 0}]
    
    form = UpdateCartForm()

    if form.validate_on_submit():
        if not any(d.get('id') == form.id.data for d in session['basket']):
            session['basket'].append({'id': form.id.data, 'quantity': form.quantity.data})
            session['basket'][0]['total_quant'] += form.quantity.data
            session.modified = True
            flash('Product added to cart')
        else:
            for d in session['basket']:
                if d.get('id') == form.id.data:
                    product = Product.query.get_or_404(form.id.data)
                    if (d.get('quantity') + form.quantity.data) <= product.stock:
                        d['quantity'] += form.quantity.data
                        session['basket'][0]['total_quant'] += form.quantity.data
                        session.modified = True
                        flash('Product added to cart')
                    else:
                        flash("You can't add that many of this item to the cart")

    return redirect(request.referrer)

@app.route("/update_cart", methods=['GET', 'POST'])
def update_cart():    
    form = UpdateCartForm()

    if form.validate_on_submit():
        if not any(d.get('id') == form.id.data for d in session['basket']):
            session['basket'].append({'id': form.id.data, 'quantity': form.quantity.data})
            session['basket'][0]['total_quant'] += form.quantity.data
            session.modified = True
            flash('Product added to cart')
        else:
            for d in session['basket']:
                if d.get('id') == form.id.data:
                    product = Product.query.get_or_404(form.id.data)
                    if form.quantity.data <= product.stock:
                        # Delete item from cart
                        if form.quantity.data < 1: 
                            quick_del_from_cart(form.id.data)
                            flash("Product removed from cart")
                        # Decrease
                        elif d['quantity'] > form.quantity.data:
                            update_val = d['quantity'] - form.quantity.data
                            session['basket'][0]['total_quant'] -= update_val # Decrease total cart quantity
                            d['quantity'] = form.quantity.data  # Decrease item cart quantity
                            flash('Your Cart was Updated')
                        # Increase
                        elif d['quantity'] < form.quantity.data:
                            update_val = form.quantity.data - d['quantity']
                            session['basket'][0]['total_quant'] += update_val # Increase total cart quantity
                            d['quantity'] = form.quantity.data # Increase item cart quantity
                            flash('Your Cart was Updated')
                            
                        session.modified = True
                    else:
                        flash("You can't add that many of this item to the cart")

    return redirect(request.referrer)

def quick_del_from_cart(product_id):
    for d in session['basket']:
        if d.get('id') == product_id:
            product = Product.query.get_or_404(product_id)
            session['basket'][0]['total_quant'] -= d['quantity']
            session['basket'].pop(session['basket'].index(d))
            session.modified = True

@app.route("/clear_the_cart", methods=['GET', 'POST'])
def clear_cart():
    try:
        session['basket'] = [{'total_quant': 0}]
        flash('Your Cart has been Cleared')
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

        
# Cart/Basket page
@app.route("/cart",  methods=['GET', 'POST'])
def cart():
    if 'basket' not in session:
        session['basket'] = [{'total_quant': 0}]
    basket_list = []
    product_details_list = []
    grand_price = 0
    item_was_removed = False
    item_quant_reduced = False

    form = UpdateCartForm()
    
    for i in range(1, len(session['basket'])):
        basket_list.append([session['basket'][i]['id'], session['basket'][i]['quantity']])

    for i in range(0, len(basket_list)):
        product = Product.query.get_or_404(basket_list[i][0])
        total_stock = product.stock

        if basket_list[i][1] <= total_stock:
            if product.discount_amount > 0:
                total_price = (product.price * basket_list[i][1]) * ((100 - product.discount_amount)/100)
            else:
                total_price = (product.price * basket_list[i][1])
            grand_price += total_price

            product_details_list.append([
                product.id,
                product.feature_image,
                product.title,
                product.price,
                product.discount_amount,
                basket_list[i][1],
                total_price,
                total_stock
            ])
        elif total_stock < 1:
            quick_del_from_cart(basket_list[i][0])
            item_was_removed = True
        elif basket_list[i][1] > total_stock:
            update_val = session['basket'][i+1]['quantity'] - total_stock
            session['basket'][0]['total_quant'] -= update_val # Decrease total cart quantity
            basket_list[i][1] -= update_val
            session['basket'][i+1]['quantity'] = basket_list[i][1]  # Decrease item cart quantity
            
            session.modified = True

            if product.discount_amount > 0:
                total_price = (product.price * basket_list[i][1]) * ((100 - product.discount_amount)/100)
            else:
                total_price = (product.price * basket_list[i][1])
            grand_price += total_price

            product_details_list.append([
                product.id,
                product.feature_image,
                product.title,
                product.price,
                product.discount_amount,
                basket_list[i][1],
                total_price,
                total_stock
            ])
            item_quant_reduced = True

    if item_was_removed: flash('One or more items in your basket has been removed')
    if item_quant_reduced: flash('The quantity of one or more items in your basket has been reduced')
    wish_list = []
    products = Product.query.filter(Product.stock > 0, Product.is_draft == 0).order_by(Product.date_listed).limit(5)
    if current_user.is_authenticated:

        wish_list = []
        wish_items = WishListItem.query.filter(WishListItem.user_id == current_user.id).all()
        # products = Product.query.join(WishListItem).filter(WishListItem == wish_items).all()
        for i in wish_items:
            prod = Product.query.filter(Product.id == i.product_id).first()
            # print(prod.id)
            wish_list.append(prod)
        print(wish_list)

    return render_template(
        'cart/cart.html',
        product_list=product_details_list,
        grand_price=grand_price,
        title='New Category',
        form=form,
        wish_list=wish_list,
        products=products
        # legend='Create a New Category',
        # items='Categories',
        # list_display=pop_categorys
    )

@app.route("/check_out", methods=['GET', 'POST'])
@login_required
def check_out():
    
    form = OrderForm()

    order_id = secrets.token_hex(10)

    if form.validate_on_submit():
        
        # for i in range(1, len(session['basket'])):
        #     order = Order(
        #         id = order_id,
        #         first_name=form.first_name.data,
        #         last_name=form.last_name.data,
        #         email=form.email.data,
        #         address_first_line=form.address_first_line.data,
        #         address_second_line=form.address_second_line.data,
        #         address_city=form.address_city.data,
        #         address_country=form.address_country.data,
        #         address_postcode=form.address_postcode.data,
        #         user=current_user
        #     )
        #     db.session.add(product)
        #     db.session.commit()
        # flash('The product was created')
        # return redirect(url_for('thank_you'))
        wish_list_item_removed = False

        for d in session['basket']:
            if WishListItem.query.filter(db.and_(WishListItem.user_id == current_user.id, WishListItem.product_id == d.get('id'))).first() is not None:
                product = WishListItem.query.filter(db.and_(WishListItem.user_id == current_user.id, WishListItem.product_id == d.get('id'))).first()
                db.session.delete(product)
                db.session.commit()
                wish_list_item_removed = True

        if wish_list_item_removed:
            flash('One or more products were removed from your Wish List')


        session['basket'] = [{'total_quant': 0}]
        return redirect(url_for('thank_you'))

    return render_template(
        'cart/check_out.html',
        title='Check Out',
        form=form,
        legend='Check out form'
    )

@app.route("/thank_you")
@login_required
def thank_you():
    return render_template(
        'cart/thank_you.html',
        title='Thank you'
    )  
# franchise_id=request.form.get('franchise'),
# pop_box_size_id=request.form.get('pop_box_size'),


#################################
#                               #
#        wish list Stuff        #
#                               #
#################################

@app.route("/add_to_wish_list", methods=['GET', 'POST'])
@login_required
def add_to_wish_list():

    form = UpdateCartForm()


    if form.validate_on_submit():
        if WishListItem.query.filter(db.and_(WishListItem.user_id == current_user.id, WishListItem.product_id == form.id.data)).first() is None:
            wish_list_item_id = secrets.token_hex(10)
            item = WishListItem (
                id = wish_list_item_id,
                product_id = form.id.data,
                user_id = current_user.id
            )
            db.session.add(item)
            db.session.commit()
            flash('Product added to your Wish List')
        else:
            flash("That product is already in your wish list")

    return redirect(request.referrer)

@app.route("/del_from_wish_list", methods=['GET', 'POST'])
@login_required
def del_from_wish_list():

    form = UpdateCartForm()


    if form.validate_on_submit():
        if WishListItem.query.filter(db.and_(WishListItem.user_id == current_user.id, WishListItem.product_id == form.id.data)).first() is not None:
            item = WishListItem.query.filter(db.and_(WishListItem.user_id == current_user.id, WishListItem.product_id == form.id.data)).first()
            db.session.delete(item)
            db.session.commit()
            flash('Product removed from your Wish List')
        else:
            flash("That product wasn't in your wish list")

    return redirect(request.referrer)
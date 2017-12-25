from flask import Flask, render_template, flash, redirect, url_for, abort
from catalog import app, db
from sqlalchemy import desc

from forms import UserForm, CategoryForm, ItemForm
from catalog.models import User, Category, Item

def get_current_user():
    user = User.query.get(1)   # 1-Samson ; 3 - Sophie
    return user


# WELCOME PAGE
@app.route('/')
def welcome():
    flash("Hello and Welcome")
    return render_template('welcome.html')

# HOME PAGE WITH CATEGORY LIST AND LATEST-ITEM LIST


@app.route('/home')
def home():
    return render_template('home.html')

# -----------------------------------------------------------------------------------------------##
# CATEGORY ELELMENTS:
# ----------------------------------------------------------------------------------------------##


@app.route('/category/list')
def category_list():
    categories = Category.query.all()
    latest_items = Item.query.order_by(Item.created.desc()).limit(2)
    return render_template('category_list.html', categories=categories,
                           items=latest_items,  user_id=get_current_user())


@app.route('/category/view/<int:category_id>')
def category_view(category_id):
    category = Category.query.get(category_id)
    items = Item.query.filter_by(category_id=category_id).order_by(Item.title).all()
    return render_template('category_view.html', items=items,
                           category=category, user_id=get_current_user())


@app.route('/category/create', methods=['GET', 'POST'])
def category_create():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category()
        category.title = form.title.data
        user = get_current_user()
        category.ctlg_user = user
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('category_list'))
    return render_template('category_create.html', form=form)


@app.route('/category/delete_confirm/<int:category_id>')
def category_delete_confirm(category_id):
    category = Category.query.filter_by(id=category_id).first()
    items = Item.query.filter_by(category_id=category_id)
    return render_template('category_delete_confirm.html',
                           category=category, items=items)


@app.route('/category/delete/<int:category_id>')
def category_delete(category_id):
    delete_flag = True
    category = Category.query.get(category_id)
    if category.ctlg_user != get_current_user():
        delete_flag = False

    items = Item.query.filter_by(category_id=category_id).all()
    for item in items:
        if item.ctlg_user != get_current_user():
            delete_flag = False
            break

    if delete_flag == True:
        for item in items:
            db.session.delete(item)
            db.session.commit()
            db.session.delete(category)
            db.session.commit()
            flash("Category -" + category.title +
                  " and all its items have been deleted successfully!!")
        return redirect(url_for('category_list'))
    else:
        return render_template('error_not_authorized.html',
                               message='Category either not created by you or has items not created by you')


@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def category_edit(category_id):
    category = Category.query.get(category_id)
    if category.ctlg_user == get_current_user():
        form = CategoryForm(obj=category)
        if form.validate_on_submit():
            form.populate_obj(category)
            db.session.add(category)
            db.session.commit()
            flash(category.title + ' updated successfully')
            return redirect(url_for('category_list'))
        return render_template('category_edit.html', form=form)
    else:
        return render_template('error_not_authorized.html',
                               message='This category is not created by you stupid!!')


# ----------------------------------------------------------------------------------------------##
# ITEMS ELEMENTS:
# ---------------------------------------------------------------------------------------------##


@app.route('/latest_items')
def latest_item():
    items = Item.query.order_by(Item.created.desc()).limit(2)
    return render_template('latest_item.html', items=items)


@app.route('/item/view/<int:item_id>')
def item_view(item_id):
    item = Item.query.get(item_id)
    return render_template('item_view.html', item=item)


@app.route('/item/create/<int:category_id>', methods=['GET', 'POST'])
def item_create(category_id):
    form = ItemForm()
    if form.validate_on_submit():
        item = Item()
        item.title = form.title.data
        item.description = form.description.data
        item.category_id = category_id
        item.ctlg_user = get_current_user()
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('item_create', category_id=category_id))
    return render_template('item_create.html', form=form, category_id=category_id)


@app.route('/item/delete_confirm/<int:item_id>')
def item_delete_confirm(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return render_template('item_delete_confirm.html')


@app.route('/item/delete/<int:item_id>')
def item_delete(item_id):
    item = Item.query.get(item_id)
    if item.user_id == get_current_user():
            db.session.delete(item)
            db.session.commit()
            return render_template('item_delete.html')

    return render_template('error_not_authorized.html', message=item.title)


@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
def item_edit(item_id):
    item = Item.query.get(item_id)
    if item.user_id == get_current_user():
        form = ItemForm(obj=item)
        if form.validate_on_submit():
            form.populate_obj(item)
            db.session.add(item)
            db.session.commit()
            flash(item.title + ' updated successfully')
            return redirect(url_for('category_view', category_id=item.category_id))
        return render_template('item_edit.html', form=form)
    return render_template('error_not_authorized.html', message=item.title)


# -------------------------------------------------------------------------------------------##
# LOGIN LOGOUT ELEMENTS:
# -------------------------------------------------------------------------------------------##

@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/user/create', methods=['GET', 'POST'])
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('user_create.html', form=form)

# -----------------------------------------------------------------------------------------##
# ERROR-TRAPPING
# -----------------------------------------------------------------------------------------##



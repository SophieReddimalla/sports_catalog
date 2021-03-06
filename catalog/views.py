# Imports from flask and sqlalchemy
import json
import random
import string
import httplib2
import requests
from flask import session as login_session
from sqlalchemy import desc
from datetime import datetime
from catalog import app, db
from forms import CategoryForm, ItemForm
from catalog.models import User, Category, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import Flask, render_template, flash, redirect, url_for, abort, \
                  jsonify, request, make_response

# Imports for the oauth

# Import from other python files


# Client_id is been retrieved from client_secrets.json file
CLIENT_ID = json.loads(
    open('/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']


# The get_current_user() gets the current user logged in based on its gplus_id
def get_current_user():
    user = None
    if 'gplus_id' in login_session:
        user = User.query.filter_by(gplus_id=str
                                    (login_session['gplus_id'])).first()
    else:
        login_session['gplus_id'] = None
    return user

# Check if user is logged in


def logged_in():
    if 'gplus_id' in login_session:
        if login_session['gplus_id']:
            return True
    return False


# WELCOME PAGE
@app.route('/')
def welcome():
    """
    This is the welcome page of the catalog project.
    """
    flash("Welcome to Sports Catalog ")
    return render_template('welcome.html')

# -----------------------------------------------------------------------------------------------##
# CATEGORY ELELMENTS:
# ----------------------------------------------------------------------------------------------##

# Displays the category list and the latest items


@app.route('/category/list')
def category_list():
    """
    This shows the list of categories and latest items in the descending
    order from the date of creation of the item. 
    """
    categories = Category.query.all()
    user = get_current_user()
    latest_items = Item.query.order_by(Item.created.desc()).limit(2)
    return render_template('category_list.html', categories=categories,
                           items=latest_items, user=user)

# Displays the items in an category


@app.route('/category/view/<int:category_id>')
def category_view(category_id):
    """
    Here the items in a particular category is displayed.
    """
    category = Category.query.get(category_id)
    items = Item.query\
                .filter_by(category_id=category_id)\
                .order_by(Item.title).all()

    return render_template('category_view.html', items=items,
                           category=category, user_id=get_current_user())

# Creates an new category


@app.route('/category/create', methods=['GET', 'POST'])
def category_create():
    """
    This creates a new category only if the user is logged in
    """
    if not logged_in():
        flash('Please log in to create categories')
        return redirect(url_for('category_list'))
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

# Delete confirmation form


@app.route('/category/delete_confirm/<int:category_id>')
def category_delete_confirm(category_id):
    """
    This shows the delete confirmation before deleting the category.
    """
    category = Category.query.filter_by(id=category_id).first()
    items = Item.query.filter_by(category_id=category_id)
    return render_template('category_delete_confirm.html',
                           category=category, items=items)

# Deletes the category and its items


@app.route('/category/delete/<int:category_id>')
def category_delete(category_id):
    """
    This deletes the category only if the user is logged in and the creator of the category.
    The category will not be deleted if it has items which are not created by the user.
    """
    if not logged_in():
        flash('Please log in to delete category')
        return redirect(url_for('category_list'))
    delete_flag = True
    # Checks if the user is the one who created the category
    category = Category.query.get(category_id)
    if category.ctlg_user != get_current_user():
        delete_flag = False

    items = Item.query.filter_by(category_id=category_id).all()
    if items is not None:
        # checks if the current category has items
        # which are not created by the user
            for item in items:
                if item.ctlg_user != get_current_user():
                    delete_flag = False
                    break
    # Deletion takes place
    if delete_flag:
        if items is not None:
            for item in items:
                db.session.delete(item)
            db.session.commit()
        db.session.delete(category)
        db.session.commit()

        flash("Category -" + category.title +
              " and all its items have been deleted successfully!!")
        return redirect(url_for('category_list'))
    else:
        flash("All that we know either that this category or its" +
              "items are not created by you hence you cannot delete it!!")
    return redirect(url_for('category_list'))

# Category can be edited here


@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def category_edit(category_id):
    """
    This creates a edits category only if the user is logged in
    """ 
    if not logged_in():
        flash('Please log in to edit categories')
        return redirect(url_for('category_list'))
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
        flash("All that we know that either this category" +
              "or its items are not created by you hence you cannot edit it!!")
    return redirect(url_for('category_list'))
# ---------------------------------------------------------------------------------------------------------------
# ITEM ELEMENTS
# --------------------------------------------------------------------------------------------------------------

# Item is been viewed


@app.route('/item/view/<int:item_id>')
def item_view(item_id):
    """
    This shows the description of the item
    """
    item = Item.query.get(item_id)
    return render_template('item_view.html', item=item)


# New item can be created
@app.route('/item/create/<int:category_id>', methods=['GET', 'POST'])
def item_create(category_id):
    """
    This creates a new item only if the user is logged in
    """
    if not logged_in():
        flash('Please log in to create items')
        return redirect(url_for('category_list'))
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
    return render_template('item_create.html',
                           form=form, category_id=category_id)

# Item deletion confirmation


@app.route('/item/delete_confirm/<int:item_id>')
def item_delete_confirm(item_id):
    """
    This shows the delete confirmation before deleting the item.
    """
    item = Item.query.get(item_id)
    return render_template('item_delete_confirm.html', item=item)

# Item deletion


@app.route('/item/delete/<int:item_id>')
def item_delete(item_id):
    """
    This deletes the item only if the user is logged in and the creator of the item.
    """
    if not logged_in():
        flash('Please log in to delete items')
        return redirect(url_for('category_list'))
    item = Item.query.get(item_id)
    category_id = item.category_id
    user = get_current_user()
    if item.user_id == user.id:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully')
        return redirect(url_for('category_view', category_id=category_id))
    else:
        flash('Item cannot be deleted!!')
        return redirect(url_for('category_view', category_id=category_id))


# Item is been edited here
@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
def item_edit(item_id):
    """
    This creates a edits category only if the user is logged in
    """ 
    if not logged_in():
        flash('Please log in to edit items')
        return redirect(url_for('category_list'))
    item = Item.query.get(item_id)
    user = get_current_user()
    if item.user_id == user.id:
        form = ItemForm(obj=item)
        if form.validate_on_submit():
            form.populate_obj(item)
            db.session.add(item)
            db.session.commit()
            flash(item.title + ' updated successfully')
            return redirect(url_for('category_view',
                                    category_id=item.category_id))
        return render_template('item_edit.html', form=form,
                               category_id=item.category_id)
    flash('You can not delete this Item its not created by you')
    return redirect(url_for('category_view', category_id=item.category_id))

# --------------------------------------------------------------------------------------------------------------
# LOGIN AND LOGOUT
# --------------------------------------------------------------------------------------------------------------


@app.route('/login')
# Here an random string is generated as state token
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state, CLIENT_ID=CLIENT_ID)


@app.route('/gconnect', methods=['POST', 'GET'])
def gconnect():
    """
    Gathers data from Google Sign In API and places it inside a session variable.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/var/www/catalog/catalog/client_secrets.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        flash('Failed to upgrade the authorization code.')
        return(url_for('welcome'))

# Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style = "width: 300px; height:300px;border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])

    # Store this User in Database if not existing
    user = User.query.filter_by(gplus_id=str(gplus_id)).first()
    if user is None:
        user = User()
        user.username = login_session['username']
        user.email = login_session['email']
        user.gplus_id = str(login_session['gplus_id'])
        user.created = datetime.utcnow()
        user.modified = datetime.utcnow()
        db.session.add(user)
        db.session.commit()

    return output


@app.route('/logout')
def logout():
    """
    This invalidate the token to prevent its misuse by clearing the session.
    """
    if login_session['access_token'] is not None:
        url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
               % login_session['access_token'])
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
    else:
        flash('You are not logged in')
        return redirect('welcome')

    # If there was an error in the access token info, abort.
    # Problems with Revoking
    # if result['status'] == '200':
    del login_session['username']
    del login_session['picture']
    del login_session['email']
    del login_session['gplus_id']
    del login_session['access_token']
    flash('Successfully Logged Out')
    # else:
    #    flash('Failed to Revoke Token')

    return redirect(url_for('welcome'))
# ---------------------------------------------------------------------------------------------------------
# JSON Endpoints
# ---------------------------------------------------------------------------------------------------------


@app.route('/api/item/view/<int:item_id>')
def api_item_view(item_id):
    """
    Returns a given item in json format.
    """
    item = Item.query.get(item_id)
    if item is None:
        data = {'error' : 'Item not found'}
        return json.dumps([data])
    return json.dumps([item.serialize])


@app.route('/api/latest-items')
def api_latest_items():
    """
    Returns Latest item list in json format.
    """
    latest_items = Item.query.order_by(Item.created.desc()).limit(2)
    if latest_items is None:
        data = {'error' : 'No Items yet'}
        return json.dumps([data])        
    return json.dumps([x.serialize for x in latest_items])

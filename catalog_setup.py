from catalog import db
from catalog.models import User, Category, Item
from datetime import datetime
# Create All Tables
print "Creating tables ..."
db.create_all()


# Create First User
print "Creating User ..."
user = User()
user.username = "Sophie Reddimalla"
user.email = "sophie.reddimalla@gmail.com"
user.gplus_id = '112241070706889739015'
user.created = datetime.utcnow()
user.modified = datetime.utcnow()
db.session.add(user)
db.session.commit()
print "User - Sophie Reddimalla created ID=" + str(user.id)


print "Creating Sample Category Football ..."
category = Category()
category.title = "Football"
category.user_id = user.id
category.created = datetime.utcnow()
category.modified = datetime.utcnow()
db.session.add(category)
db.session.commit()
print "Category - Football created ID=" + str(category.id)


print "Creating Sample Items in Football ..."
item = Item()
item.category_id = category.id
item.title = "Soccer Ball"
item.description = "High Quality ,Tournament grade"
item.created = datetime.utcnow()
item.modified = datetime.utcnow()
item.user_id = user.id
db.session.add(item)
db.session.commit()
print "Item - %s created ID=%d" % (item.title, item.id)

print "Creating Sample Items in Football ..."
item = Item()
item.category_id = category.id
item.title = "Studs - Reebok"
item.description = "Imported Studs from Taiwan"
item.created = datetime.utcnow()
item.modified = datetime.utcnow()
item.user_id = user.id
db.session.add(item)
db.session.commit()
print "Item - %s created ID=%d" % (item.title, item.id)
print "Done!!!"

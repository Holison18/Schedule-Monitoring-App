from app import db
from app.models import Admin

# This creates your admin user. You can change the username if you like.
admin_user = Admin(username='admin')

# This sets the password securely.
admin_user.set_password('BecauseHeLives@2025')

# Add to the database and save.
db.session.add(admin_user)
db.session.commit()

print("Admin user 'admin' created successfully.")
exit()
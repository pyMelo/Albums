import os
import django
from faker import Faker
from django.contrib.auth.models import User

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
# Number of users to generate
num_users = 10

# Create Faker instance
fake = Faker()

# Generate and add users to the database
for _ in range(num_users):
    # Generate random username and email
    username = fake.user_name()
    email = fake.email()

    # Create a new user
    user = User.objects.create_user(username=username, email=email, password='asdasd99')

    print(f"User created: {user.username} - {user.email}")

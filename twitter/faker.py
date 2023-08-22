from faker import Faker


from django.contrib.auth.models import User

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter.settings')
# django.setup()

def generate_fake_users(num_users):
    fake = Faker()

    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        print(f"Generated user: {username}, {email}, {password}")

if __name__ == '__main__':
    num_users = 10  # Change this to the desired number of users
    generate_fake_users(num_users)
    print(f"{num_users} fake users generated.")
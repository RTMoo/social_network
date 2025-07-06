from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Создает 10 тестовых пользователей с email_verified=True"

    def handle(self, *args, **options):
        created_count = 0

        for i in range(1, 11):
            username = f"user{i}"
            email = f"user{i}@a.com"
            password = "admin"

            # Проверяем, существует ли пользователь
            if CustomUser.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Пользователь {username} уже существует, пропускаем"
                    )
                )
                continue

            # Создаем пользователя
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password
            )

            # Устанавливаем email_verified=True
            user.email_verified = True
            user.save()

            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f"Создан пользователь: {username} ({email})")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Готово! Создано {created_count} пользователей")
        )

        if created_count > 0:
            self.stdout.write(self.style.SUCCESS("Данные для входа:"))
            for i in range(1, created_count + 1):
                self.stdout.write(f"  user{i}a.com / admin")

from django.db import models


class User(models.Model):
    class Meta:
        db_table = 'users'
        ordering = ['created_at']
        verbose_name = 'Пользователи'
        verbose_name_plural = verbose_name

    user_id = models.BigIntegerField(primary_key=True, db_index=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    is_registered_meditation = models.BooleanField(default=False, verbose_name='Медитации')
    is_registered_days = models.BooleanField(default=False, verbose_name='Счастливые дни')
    is_user_agreement_accepted = models.BooleanField(default=False, verbose_name='Пользовательское соглашение')
    fio = models.CharField(max_length=64, null=True, blank=True)
    email = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    status = models.CharField(max_length=32, null=True, blank=True)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    language_code = models.CharField(max_length=2, null=True, blank=True)
    is_premium = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


class SupportRequest(models.Model):
    class Meta:
        db_table = 'support_requests'
        ordering = ['id']
        verbose_name = 'Запросы в поддержку'
        verbose_name_plural = verbose_name

    id = models.IntegerField(primary_key=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class Dispatcher(models.Model):
    class Meta:
        db_table = 'mailings'
        ordering = ['id']
        verbose_name = 'Рассылки'
        verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', to_field='id', on_delete=models.CASCADE)
    is_registered_meditation = models.BooleanField(default=False, verbose_name='Медитации')
    is_registered_days = models.BooleanField(default=False, verbose_name='Счастливые даты')
    is_for_all_users = models.BooleanField(default=False, verbose_name='Всем пользователям')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    send_at = models.DateTimeField()

    def __str__(self):
        return f'{self.id}'


class Post(models.Model):
    class Meta:
        db_table = 'static_content'
        ordering = ['id']
        verbose_name = 'Контент для рассылок'
        verbose_name_plural = verbose_name

    id = models.BigIntegerField(primary_key=True)
    text = models.TextField(blank=True, null=True)
    photo_file_id = models.CharField(max_length=256, blank=True, null=True)
    video_file_id = models.CharField(max_length=256, blank=True, null=True)
    video_note_id = models.CharField(max_length=256, blank=True, null=True)
    document_file_id = models.CharField(max_length=256, blank=True, null=True)
    sticker_file_id = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

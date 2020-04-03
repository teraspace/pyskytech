from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_login = models.CharField(max_length=255)
    encrypted_password = models.CharField(max_length=255)
    reset_password_token = models.CharField(max_length=255)
    reset_password_sent_at = models.DateTimeField(db_column='reset_password_sent_at')
    remember_created_at = models.DateTimeField(db_column='reset_password_sent_at')
    sign_in_count = models.IntegerField()
    current_sign_in_at = models.DateTimeField(db_column='current_sign_in_at')
    last_sign_in_at = models.DateTimeField(db_column='last_sign_in_at')
    current_sign_in_ip = models.CharField(max_length=255)
    last_sign_in_ip = models.CharField(max_length=255)
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at')
    full_name = models.CharField(max_length=255)
    user_state = models.BooleanField()
    date_start = models.DateTimeField(db_column='date_start')
    date_end = models.DateTimeField(db_column='date_end')
    user_profile_id = models.IntegerField()
    owner_id = models.IntegerField()
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    profile = models.IntegerField()
    user_group_profile_id = models.IntegerField()
    image_file_name = models.CharField(max_length=255)
    image_content_type = models.CharField(max_length=255)
    image_file_size = models.IntegerField()
    image_updated_at = models.DateTimeField(db_column='image_updated_at')
    image = models.CharField(max_length=900)
    user_create = models.CharField(max_length=100)
    user_update = models.CharField(max_length=100)
    date_update = models.DateTimeField(db_column='date_update')
    date_create = models.DateTimeField(db_column='date_create')
    walkthrough = models.BooleanField()
    locale = models.CharField(max_length=2)
    homologo = models.IntegerField()
    new = models.BooleanField()
    warehouse = models.CharField(max_length=50)
    confirmation_code = models.CharField(max_length=4)
    identification = models.CharField(max_length=15)
    wait_alarm = models.IntegerField()
    time_zone= models.CharField(max_length=50)

    class Meta:
        db_table = "users"

class OauthAccessToken(models.Model):
    id = models.IntegerField(primary_key=True)
    resource_owner_id = models.IntegerField()
    application_id = models.IntegerField()
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    revoked_at= models.DateTimeField(db_column='date_update')
    created_at= models.DateTimeField(db_column='date_update')
    scopes = models.CharField(max_length=255)
    previous_refresh_token = models.CharField(max_length=100)
    user_create = models.CharField(max_length=100)
    user_update = models.CharField(max_length=100)
    date_update = models.DateField(db_column='date_update')
    date_create = models.DateField(db_column='date_update')

    class Meta:
        db_table = "OAUTH_ACCESS_TOKENS"

class State(models.Model):
    print('State')
    id = models.IntegerField(primary_key=True)
    color = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    class Meta:
        db_table = "STATES"

class OwnerPlate(models.Model):
    id = models.IntegerField(primary_key=True)
    plate =  models.CharField(max_length=50)
    owner_id = models.IntegerField()
    type_plate = models.CharField(max_length=2)
    class Meta:
        db_table = "OWNER_PLATES"

class Mobile(models.Model):
    id = models.IntegerField(primary_key=True)
    plate =  models.CharField(max_length=50)
    class Meta:
        db_table = "MOBILES"    

class UserSupport(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    owner_id = models.IntegerField()
    token = models.CharField(max_length=255)
    ip = models.CharField(max_length=50)
    date_entry = models.DateTimeField(db_column='date_entry')
    class Meta:
        db_table = "USER_SUPPORTS"    
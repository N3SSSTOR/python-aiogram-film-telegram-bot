from peewee import * 


db = SqliteDatabase(database="app/database/database.db")


class BaseModel(Model):
    class Meta:
        database = db 


class User(BaseModel):
    telegram_id = BigIntegerField()
    date = CharField(max_length=100)
    captcha_status = IntegerField(default=0)
    last_captcha_time = CharField(max_length=100, null=True)
    captcha_text = CharField(max_length=100, null=True)
    subscribe_status = IntegerField(default=0)
    wait_check = IntegerField(default=0)
    lang = CharField(max_length=3, default="RU")
    discount = IntegerField(default=0)
    self_ref_url = CharField(max_length=100)
    balance = IntegerField(default=0)
    membered = BooleanField(default=False)

    class Meta:
        db_table = "users"


class Movie(BaseModel):
    name = CharField(max_length=100)
    description = TextField()
    img_url = TextField()
    tags = TextField()

    class Meta:
        db_table = "movies"


class Token(BaseModel):
    telegram_token = TextField()
    user_id = BigIntegerField()

    class Meta:
        db_table = "tokens"


if __name__ == "__main__":
    db.create_tables([User, Movie, Token])
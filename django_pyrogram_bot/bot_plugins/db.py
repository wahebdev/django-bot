from asgiref.sync import sync_to_async

from bot.models import TelegramUser, TelegramUserHistory, models, BaseModel

#start_bot
@sync_to_async
def insert(id, username, name):
    TelegramUser(user_id=id,username=username,first_name=name).save()



@sync_to_async
def search(id):
    return TelegramUser.objects.filter(user_id=id).values()[0]

@sync_to_async
def usage_change(id, duration):
    user:TelegramUser=TelegramUser.objects.get(user_id=id)
    user.usage=duration
    user.save()


@sync_to_async
def usage(id):
    return TelegramUser.objects.filter(user_id=id).values()[0]['usage']

@sync_to_async
def ban_change(id, ban):
    user: TelegramUser = TelegramUser.objects.get(user_id=id)
    user.block = ban
    user.save()

@sync_to_async
def ban(id):
    ban_change(id, True)

@sync_to_async
def unban(id):
    ban_change(id, False)

@sync_to_async
def is_ban(id):
    return TelegramUser.objects.filter(user_id=id).values()[0]['block']

@sync_to_async
def admin_change(id, admin):
    user: TelegramUser = TelegramUser.objects.get(user_id=id)
    user.admin = admin
    user.save()

@sync_to_async
def admin(id):
    admin_change(id, True)

@sync_to_async
def unadmin(id):
    admin_change(id, False)

@sync_to_async
def is_admin(id):
    return TelegramUser.objects.filter(user_id=id).values()[0]['admin']




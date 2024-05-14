from django.contrib.auth.signals import user_logged_in
import logging


logging.basicConfig(level='DEBUG')
logger = logging.getLogger("my_signals")


# сделать логгирование для получения токена в djoser
def my_login_handler(sender, user, request, **kwargs):
    logger.debug(f'User(not social) {user.username} logged in')


user_logged_in.connect(my_login_handler)

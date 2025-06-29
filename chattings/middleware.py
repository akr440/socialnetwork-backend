# chat/middleware.py
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import InvalidTokenError

@database_sync_to_async
def get_user(validated_token):
    try:
        return JWTAuthentication().get_user(validated_token)
    except:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        token = parse_qs(query_string).get("token", [None])[0]

        if token is not None:
            try:
                validated_token = JWTAuthentication().get_validated_token(token)
                scope["user"] = await get_user(validated_token)
            except InvalidTokenError:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        close_old_connections()
        return await super().__call__(scope, receive, send)
from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    @staticmethod
    def get_refresh_token_string(request) -> str:
        if request.headers.get("X-Client-Type") == "mobile":
            return request.headers.get("Token")
        return request.COOKIES.get("refresh")

    @classmethod
    def refresh_access_token(cls, request) -> str:
        token_str = cls.get_refresh_token_string(request)
        if not token_str:
            raise ValueError("Refresh token missing")
        refresh = RefreshToken(token_str)
        return str(refresh.access_token)

    @classmethod
    def logout(cls, request):
        token_str = cls.get_refresh_token_string(request)
        if token_str:
            token = RefreshToken(token_str)
            token.blacklist()

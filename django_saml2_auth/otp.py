import jwt
import hashlib
from urllib.parse import urlparse, urlunparse
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings

from .utils import get_reverse


class DatetimeProvider:
    def now(self) -> datetime:
        return datetime.now(tz=timezone.utc)


class OTPService:
    def __init__(self):
        self.datetime_provider = DatetimeProvider()

    def is_otp_server(self, request):
        return settings.SAML2_AUTH.get("OTP_SERVER") == request.get_host()

    def generate_fingerprint(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        key = f"{ip}{user_agent}"
        return hashlib.sha256(key.encode()).hexdigest()

    def get_otp_endpoint(self, user, next_url: str, token: str) -> str:
        new_query = f"token={token}&uid={user.id}"
        new_path = get_reverse(["django_saml2_auth:otp_login"])
        parsed_url = urlparse(next_url)
        return urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            new_path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))

    def generate_otp(
        self,
        user,
        fingerprint: str,
        next_url: str,
    ) -> str:
        iat = self.datetime_provider.now()
        exp = iat + timedelta(seconds=30)
        return jwt.encode(
            {
                "sub": f"{user.id}",
                "iat": iat.timestamp(),
                "exp": exp.timestamp(),
                "fingerprint": fingerprint,
                "next_url": next_url,
            },
            # If a user changes their password, invalidates all of their tokens.
            user.password,
            algorithm="HS256",
            headers={"alg": "HS256", "typ": "JWT"},
        )

    def validate_otp(
        self,
        user,
        fingerprint: str,
        token: str,
    ) -> str:
        data = jwt.decode(
            token,
            user.password,
            algorithms=["HS256"],
            issuer="passthrough",
            options={
                "verify_signature": True,
                "verify_iat": True,
                "verify_exp": True,
            },
        )

        if data["sub"] != f"{user.id}":
            raise ValueError("Invalid user ID")

        if data["fingerprint"] != fingerprint:
            raise ValueError("Invalid fingerprint")
    
        return data["next_url"]

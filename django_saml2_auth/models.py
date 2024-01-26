from django.db import models
from uuid import uuid4

class SamlMetaData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    metadata_contents = models.TextField(blank=True)
    email_domain = models.TextField()
    host_name = models.TextField(
        null=True,
        blank=True, 
        help_text=(
            "e.g. test.example.com. When populated, only requests coming "
            "from a specific host will have SAML enabled."
        ),
    )

    enable_saml = models.BooleanField(
        blank=True, 
        null=True,
        default=False,
    )
    enable_optional_saml = models.BooleanField(
        blank=True, 
        null=True,
        default=False,
        help_text=(
            "when False, SAML is forced if it is enabled. "
            "When True, SAML is optional when it is enabled."
        ),
    )

    def __str__(self):
        return f"<SAML Metadata: {self.email_domain}>"

    class Meta(models.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["email_domain", "host_name"],
                name="unique_email_host_name",
            )
        ]
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from profiles.models import Profile

profile_index = Index("profiles")

profile_index.settings(number_of_shards=1, number_of_replicas=0)


@registry.register_document
class ProfileDocument(Document):
    profile_id = fields.IntegerField(
        attr="id",
    )
    username = fields.TextField(attr="user.username")

    class Index:
        name = "profiles"

    class Django:
        model = Profile

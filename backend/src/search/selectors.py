from search.documents import ProfileDocument
from elasticsearch_dsl.query import Q
from profiles.selectors import get_profiles_with_id
from typing import List
from profiles.models import Profile


def search_profiles(query: str) -> List[Profile]:
    """
    Выполняет поиск профилей пользователей по заданному запросу.

    Args:
        query (str): Строка поиска, по которой будет осуществляться поиск пользователей по username.

    Returns:
        List[Profile]: Список объектов профиля, отсортированных по релевантности (соответствию поисковому запросу).
    """

    if not query:
        return []

    query = query.strip()
    profiles_size = 10

    search = ProfileDocument.search().query(
        Q("match_phrase_prefix", username=query),
    )[:profiles_size]

    response = search.execute()

    profile_ids = [profile.profile_id for profile in response]
    profiles = get_profiles_with_id(ids=profile_ids)

    # сохранить порядок по релевантности (hit score)
    id_order = {id_: i for i, id_ in enumerate(profile_ids)}
    profiles = sorted(profiles, key=lambda p: id_order[p.id])

    return profiles

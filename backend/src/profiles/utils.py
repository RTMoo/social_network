import uuid


def upload_to(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return f"profiles/avatars/{new_filename}"

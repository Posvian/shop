from django.core.exceptions import ValidationError


def validate_size_image(file_object):
    """
    Проверка размера файла
    """
    megabyte_limit = 5
    if file_object.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {megabyte_limit}MB")

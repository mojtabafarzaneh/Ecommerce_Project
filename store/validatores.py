from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 50
    
    if file.size > max_size_kb:
        raise ValidationError(f"the size of the file couldn't be more than {max_size_kb}KB!")
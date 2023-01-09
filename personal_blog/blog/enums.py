from enumfields import Enum


class PostStatus(Enum):
    DRAFT = 'DF'
    PUBLISHED = 'PB'

    class Labels:
        DRAFT = 'Draft'
        PUBLISHED = 'Published'

import math


def add_pagination(query, page, page_size):
    if page is not None:
        total_items = query.count()
        query = query.offset(page_size * (page - 1)).limit(page_size)
        total_pages = math.ceil(total_items / page_size)
    return query, total_items, total_pages

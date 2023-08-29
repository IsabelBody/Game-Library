
def paginate(items, page):
    items_per_page = 21
    total_items = len(items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start = (page - 1) * items_per_page
    end = start + items_per_page
    displayed_items = items[start:end]
    return displayed_items, total_pages, start, end

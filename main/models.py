class PageRequest: 
    # def __init__(self, page, row_size, page_size, total_rows, total_pages, row_start, row_end, page_start, page_end, is_first, is_last, has_previous, has_next):
    #     self.page = page
    #     self.row_size = row_size
    #     self.page_size = page_size
    #     self.total_rows = total_rows
    #     self.total_pages = total_pages
    #     self.row_start = row_start
    #     self.row_end = row_end
    #     self.page_start = page_start
    #     self.page_end = page_end
    #     self.is_first = is_first
    #     self.is_last = is_last
    #     self.has_previous = has_previous
    #     self.has_next = has_next
    def __init__(self, page, row_size, page_size, total_rows, total_pages, row_start, row_end, page_start, page_end, is_first, is_last, has_previous, has_next):
        self.page = page if page is not None else 1
        self.row_size = row_size if row_size is not None else 10
        self.page_size = 10
        self.isCount = True
        self.row_start = row_start
        self.row_end = row_end
        self.page_start = page_start
        self.page_end = page_end
        self.is_first = is_first
        self.is_last = is_last
        self.has_previous = has_previous
        self.has_next = has_next
    

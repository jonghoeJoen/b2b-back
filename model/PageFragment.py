
# def limitOffset(): 
#     return "LIMIT %s OFFSET %s"

# def countStart():
#     return "SELECT COUNT(*) AS `total_rows` FROM ("

# def countEnd():
#     return ") `count_query`"

# def sortStart():
#     return "SELECT * FROM ("

# def sortStartRowNumber(sortList): 
#     return "SELECT * , ROW_NUMBER() OVER () SEPARATE_NUM"

# def sortEnd(sortList):
#     query = " ) `sort_query`"
#     if sortList != None:
#         query += " ORDER BY"
#         for i, sort in sortList: 
#             query += ' sort_query.%s'
#             if (i==len(sortList)-1):
#                 if ssprt

#     return ""
#[option, scoring]

# def plurality_opti(vote_class=None):
#     def gen_vect(r):
#         if len(r[0]) == 1:
#             res = [1]
#             res.extend([0 for n in range(vote_class.max_len_of-1)])
#         else:
#             res = [1 for i in range(len(r[0]))]
#             res.extend([0 for n in range(vote_class.max_len_of-len(r[0]))])
#         return res
#     return [3, gen_vect]
#     # return [3, 
#     #         [1,1,0]]

# def plurality_tie(vote_class=None):
#     def gen_vect(r):
#         res = [1]
#         res.extend([0 for n in range(vote_class.max_len_of-1)])
#         return res
#     return [3, gen_vect]

# def borda_opti(vote_class):
#     """
#     vote_class : voting method class with the attribute max_len_of updated
#     """
#     def gen_vect_nbf(r):
#         """
#         generate depending on the length of fact in the object (fact in the ranking to be more precise)
#         r : ranking
#         """
#         if type(r) == int:
#             x = r
#         else:
#             x = sum([len(l) for l in r])
#         if x == 0:
#             return []
#         if x == 1:
#             if vote_class.max_len_of == 1:
#                 return [1]
#             return [vote_class.max_len_of-1]
#         v = [i for i in range(vote_class.max_len_of-1, vote_class.max_len_of-x-1, -1)]
#         return v
    
#     return [3, gen_vect_nbf]
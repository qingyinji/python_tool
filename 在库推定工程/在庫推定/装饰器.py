from copy import deepcopy
import 在庫推定.数据变换 as Change


def cache_fit(fun):
    cache_temp = []
    cache_tempA = []
    cache_tempB = []
    cache_tempC = []

    def wrapper(self, data):
        if data[0] != 0:
            # data = Change.data_change(data)
            # cache_temp.append(deepcopy(data))

            cache_tempA.append(deepcopy(data[0]))
            cache_tempB.append(deepcopy(data[1]))
            cache_tempC.append(deepcopy(data[2]))
            return
        # fun(self, deepcopy(cache_temp))
        fun(self, [deepcopy(cache_tempA), deepcopy(cache_tempB), deepcopy(cache_tempC)])
        cache_temp.clear()

        cache_tempA.clear()
        cache_tempB.clear()
        cache_tempC.clear()
    return wrapper


def cache_pre(fun):
    cache_tempA = []
    cache_tempB = []
    cache_tempC = []

    def wrapper(self, data):
        if data[0] != 0:
            cache_tempA.append(deepcopy(data[0]))
            cache_tempB.append(deepcopy(data[1]))
            cache_tempC.append(deepcopy(data[2]))
            ret = fun(self, deepcopy(cache_tempA), deepcopy(cache_tempB), deepcopy(cache_tempC))
            return ret
        fun(self, deepcopy(cache_tempA), deepcopy(cache_tempB), deepcopy(cache_tempC), last=True)
        cache_tempA.clear()
        cache_tempB.clear()
        cache_tempC.clear()
        return None
    return wrapper
# def cache_pre(fun):
#     cache_temp = []
#
#     def wrapper(self, data):
#         if data[0] != 0:
#             data = Change.data_change(data)
#             cache_temp.append(deepcopy(data))
#             ret = fun(self, deepcopy(cache_temp))
#             return ret
#         fun(self, deepcopy(cache_temp), last=True)
#         cache_temp.clear()
#         return None
#     return wrapper
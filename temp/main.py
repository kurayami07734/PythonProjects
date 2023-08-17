from http import cookies


def dist(a: list[int]) -> int:
    ans = 0
    for i in range(1, len(a)):
        if (a[i - 1] == a[i]):
            ans += 2
        else:
            ans += 1
    return ans


def solve(n: int, k: int, s: str, q: list[int]) -> list[int]:
    res = []
    state = list(s)
    d = dist(state)
    for i in q:
        state[i - 1] = '1' if state[i - 1] == '0' else '0'

        res.append()
    return res


# print(solve(4, 2, '0110', [2, 3]))


c = cookies.SimpleCookie()
c['cookie1'] = 'value1'
c['cookie1']['path1'] = '/example1/'
c['cookie2'] = 'value2'
c['cookie2']['path2'] = '/example2/'
h_c = c.output(attrs=['path2'], header='Cookie')
print(h_c)

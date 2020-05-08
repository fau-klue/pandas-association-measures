#cython: cdivision=True

cpdef double choose(int n, int k):
    """
    Binomial coefficient Cython implementation
    :param int n: n elements
    :param int k: k subset elements
    :rtype: int
    """

    if k < 0:
        return 0
    if k == 0:
        return 1
    if n < k:
        return 0

    cdef double p = 1
    cdef int N = min(k, n - k) + 1
    cdef int i
    for i in range(1, N):
        p *= n
        p = int(p / i)
        n -= 1
    return p
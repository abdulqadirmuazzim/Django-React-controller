import numpy as np
import fractions as fr

A = [[1, -3, 1], [2, -8, 8], [-6, 3, -15]]

A = np.array(A)

b = np.array([4, -2, 9])


ans = np.linalg.solve(A, b)
print(ans)

array1 = np.array(
    [
        [2, -3, 1],
        [-2, -1, 4],
        [0, 2, 2],
    ]
)

array2 = np.array([[3, -2, 1], [1, -1, 2], [-2, 2, 0]])

ans2 = np.dot(array1, array2)

print("Second answer", ans2)
# np.gradient()

matrix = np.array([[2, 4, -2], [-2, 0, 1], [3, -3, 0]])
inverse = np.linalg.inv(matrix)
print("inverse is:", inverse)

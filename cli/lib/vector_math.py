def add_vectors(vec1: list[float], vec2: list[float]) -> list[float]:
    if len(vec1) != len(vec2):
        raise ValueError('vectors must have same length')

    result = []
    for i in range (len(vec1)):
        result.append(vec1[i] + vec2[i])

    return result

def subtract_vectors(vec1: list[float], vec2: list[float]) -> list[float]:
    if len(vec1) != len(vec2):
        raise ValueError('vectors must have same length')

    result = []
    for i in range(len(vec1)):
        result.append(vec1[i] - vec2[i])

    return result

def dot(vec1: list[float], vec2: list[float]) -> float:
    if len(vec1) != len(vec2):
        raise ValueError('vectors must have same length')

    result = 0.0
    for i in range(len(vec1)):
        result += vec1[i] * vec2[i]

    return result

def euclidean_norm(vec: list[float]) -> float:
    total = 0.0
    for x in vec:
        total += x**2

    return total**0.5

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    if len(vec1) != len(vec2):
        raise ValueError('vectors must have same length')

    dot_product = dot(vec1, vec2)
    mag_vec1 = euclidean_norm(vec1)
    mag_vec2 = euclidean_norm(vec2)

    if mag_vec1 == 0 or mag_vec2 == 0:
        return 0.0

    return dot_product / (mag_vec1 * mag_vec2)


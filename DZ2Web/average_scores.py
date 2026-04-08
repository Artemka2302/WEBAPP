def compute_average_scores(scores):
    if not scores:
        raise ValueError("scores cannot be empty")

    X = len(scores)
    N = len(scores[0])

    if not (0 < N <= 100 and 0 < X <= 100):
        raise ValueError("N and X must be between 1 and 100")

    # проверка одинаковой длины
    for subject in scores:
        if len(subject) != N:
            raise ValueError("All tuples must have same length")

        # проверка диапазона оценок
        for score in subject:
            if not (0 <= score <= 100):
                raise ValueError("Score must be between 0 and 100")

    averages = []
    for student_scores in zip(*scores):
        avg = round(sum(student_scores) / len(student_scores), 1)
        averages.append(avg)

    return tuple(averages)
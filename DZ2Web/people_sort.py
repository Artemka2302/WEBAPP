import operator

def person_lister(f):
    def inner(people):
        if not (1 <= len(people) <= 10):
            raise ValueError("Количество человек должно быть от 1 до 10")
        people_sorted = sorted(people, key=operator.itemgetter(2))
        return [f(p) for p in people_sorted]
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    people = [input().split() for i in range(int(input()))]
    print(*name_format(people), sep='\n')

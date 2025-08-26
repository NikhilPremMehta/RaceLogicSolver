import itertools


class And():
    def __init__(self, *conjuncts):
        self.conjuncts = list(conjuncts)

    def evaluate(self, model):
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def add(self, conjuct):
        self.conjuncts.append(conjuct)


class Or():
    def __init__(self, *conjucts):
        self.conjunts = list(conjucts)

    def evaluate(self, model):
        return any(conjunct.evaluate(model) for conjunct in self.conjuncts)


class Biconditional():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, model):
        return ((self.left.evaluate(model)
                 and self.right.evaluate(model))
                or (not self.left.evaluate(model)
                    and not self.right.evaluate(model)))


class Behind():
    def __init__(self, behind, ahead):
        self.ahead = ahead
        self.behind = behind

    def evaluate(self, model):
        return model[self.behind.index] == model[self.ahead.index] + 1


class Position():
    def __init__(self, person, pos):
        self.person = person
        self.pos = pos

    def evaluate(self, model):
        return model[self.person.index] == self.pos


class Wrong():
    def __init__(self, person):
        self.person = person

    def evaluate(self, model):
        return model[model[0]] == self.person


class Right():
    def __init__(self, person):
        self.person = person

    def evaluate(self, model):
        return model[0] != self.person.index


class Person():
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __str__(self):
        return str([self.name, self.index])

    def __repr__(self):
        return str([self.name, self.index])


def model_check(knowledge, people):
    model = []
    sus = set()
    for i in range(len(people)):
        model.append(i + 1)
    m = itertools.permutations(model)
    for model in m:
        model = list(model)
        for i in range(len(people)):
            model.insert(0, i + 1)
            if knowledge.evaluate(model):
                sus.add(people[i])
            model.pop(0)
    return sus


def findOutMrWrong(conversation):
    knowledge = And()
    people = []
    for line in conversation:
        name = line[:line.find(":")]
        if not any(p.name == name for p in people):
            person = Person(name, len(people) + 1)
            people.append(person)  # 0th position is who's mr wrong

    for line in conversation:
        person = next(i for i in people if i.name == line[:line.find(":")])
        line = line[len(person.name) + 1:]
        if line[:6] == "I'm in":
            place = int(''.join(x for x in line if x.isdigit()))
            knowledge.add(Biconditional(Right(person), Position(person, place)))
        elif line[:14] == "The man behind":
            other = next(i for i in people if i.name == line[21:-1])
            knowledge.add(Biconditional(Right(person), Behind(other, person)))
        elif line[:16] == "The man in front":
            other = next(i for i in people if i.name == line[26:-1])
            knowledge.add(Biconditional(Right(person), Behind(person, other)))
        elif line[-12:] == "front of me.":
            place = int(''.join(x for x in line if x.isdigit())) + 1
            knowledge.add(Biconditional(Right(person), Position(person, place)))
        elif line[-10:] == "behind me.":
            place = len(people) - int(''.join(x for x in line if x.isdigit()))
            knowledge.add(Biconditional(Right(person), Position(person, place)))
    results = model_check(knowledge, people)
    return list(results)[0].name if len(results) == 1 else None


testInput = conversation = [ #Tom
    "John:I'm in 1st position.",
    "Peter:I'm in 2nd position.",
    "Tom:I'm in 1st position.",
    "Peter:The man behind me is Tom.",
    "Tim:The man in front of me is Tom."
]
testInput2 = [ #John
    "John:I'm in 1st position.",
    "Peter:I'm in 2nd position.",
    "Tom:I'm in 1st position.",
    "Peter:The man in front of me is Tom."
]

testInput3 = [ #Tom
    "John:I'm in 1st position.",
    "Peter:There is 1 people in front of me.",
    "Tom:There are 2 people behind me.",
    "Peter:The man behind me is Tom."
]

testInput4=[ #None
    "John:The man behind me is Peter.",
    "Peter:There is 1 people in front of me.",
    "Tom:There are 2 people behind me.",
    "Peter:The man behind me is Tom."
]

testInput5 = [ #Szoxdouot
    "Ugclpsp:The man behind me is Eaoujalm.",
    "Szoxdouot:The man in front of me is Szoxdouot.",
    "Eaoujalm:The man in front of me is Ugclpsp.",
    "Emuy:The man behind me is Ugclpsp."
]


print(findOutMrWrong(testInput3))

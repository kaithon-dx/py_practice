import random

def get_answer(answer_number):
    if answer_number == 1:
        return '確かにそうだ'
    elif answer_number == 2:
        return '間違いなくそうだ'
    elif answer_number == 3:
        return 'はい'
    elif answer_number == 4:
        return 'もういちどやってみて'
    elif answer_number == 5:
        return '後で聞いてくれ'
    elif answer_number == 6:
        return '集中して聞いてみて'
    elif answer_number == 7:
        return '私の答えはノーです'
    elif answer_number == 8:
        return '見通しはそれほど良くない'
    elif answer_number == 9:
        return '非常に疑わしい'

r = random.randint(1,9) #1も9も含まれる
fortune = get_answer(r)
print(fortune)
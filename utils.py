import random

from datacenter.models import Lesson, Mark, Chastisement, Commendation, Schoolkid
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

COMMENDATIONS = [
    'Хвалю!',
    'Молодец!',
    'Ребенок хорошо себя проявил!',
    'Пример для подражания!',
    'Хорошо себя вел'
]

def get_schoolkid(schoolkid_name): 
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        raise Exception('Ученик не найден! Попробуй с другим именем.')
    except MultipleObjectsReturned:
        return Exception('Найдено несколько учеников! Укажи имя точнее.')
    return schoolkid

def fix_marks(schoolkid_name):
    Mark.objects.filter(schoolkid=get_schoolkid(schoolkid_name), points__in=[2,3]).update(points=5)

def remove_chastisements(schoolkid_name):
    Chastisement.objects.filter(schoolkid=get_schoolkid(schoolkid_name)).delete()

def count_bad_marks(schoolkid_name):
    print(Mark.objects.filter(schoolkid=get_schoolkid(schoolkid_name), points__in=[2,3]).count())

def create_commendation(schoolkid_name, lesson_title):
    schoolkid = get_schoolkid(schoolkid_name)
    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=lesson_title
    ).last()

    if not last_lesson:
        raise Exception('Урок не найден! Возможно предмет указан неправильно.')
    
    Commendation.objects.create(
        text=random.choice(COMMENDATIONS),
        schoolkid=schoolkid,
        created=last_lesson.date,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )

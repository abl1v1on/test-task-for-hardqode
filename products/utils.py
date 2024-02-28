from .models import Product, Group


def get_all_products():
    return Product.objects.all()


def group_count(product):
    """
    Функция возвращает кол-во групп связанных с определенным курсом
    """
    return Group.objects.filter(product_id=product.id).count()


# ИЗМЕНИТЬ НАЗВАНИЕ
def check(product, user):
    """
    Функция для проверки, записан ли пользователь на курс.
    Если записан, то вернет True, иначе False
    """
    if not product.group_product.last():
        return False
    elif user in product.group_product.last().students.all():
        return True
    return False


def create_group(product):
    Group.objects.create(
        group_name=f'{product.product_name} - группа {group_count(product) + 1}',
        product_id=product.id
    )       


def add_user_in_group(product, user):
    # Если групп связанных с курсом (product) в бд ещё нету, то создаем первую группу
    if group_count(product) == 0:
        create_group(product=product)

    # Получаем объект последней группы связанной с курсом
    group = Group.objects.filter(product_id=product.id).last()
    # Получаем кол-во студентов из раннее полученной группы
    quantity_students_in_group = group.students.count()

    """
    Проверяем, не превышает ли кол-во студентов крайней группы
    значение поля max_student_quantity. Если 'лимит' превышен, то
    мы вновь вызываем функцию create_group и создаем новую группу
    """
    if quantity_students_in_group >= product.max_student_quantity:
        create_group(product=product)
        group = Group.objects.filter(product_id=product.id).last()
        group.students.add(user)
    else:
        """
        Добавляем студента в группу. Если он уже есть в группе,
        то ничего не произойдет, студент никуда не попадет.
        """ 
        group.students.add(user)


    # # Если групп в бд ещё нету, то создаем первую группу
    # if group_count() == 0:
    #     create_group(product=product)
    # # Получаем объект последней группы
    # group = Group.objects.filter(product_id=product.id).last()
    # # Кол-во студентов в группе
    # quantity_students_in_group = group.students.count()

    # if quantity_students_in_group >= product.max_student_quantity:
    #     pass

    # if user not in group.students.all():
    #     group.students.add(user)
    # else:
    #     print('AAAAAAAAAAAAAAAAAAAAAA', end='\n\n\n\n\n\n\n\n\n')
    # Group.objects.get(product_id=product.id).students.add(user)

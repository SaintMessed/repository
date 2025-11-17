class User:
    # атрибут класса — количество обычных пользователей
    count = 0

    def __init__(self, name: str, login: str, password: str, level: int):
        self._name = name
        self._login = login
        self._password = password
        self._level = level   # «уровень» для сравнения пользователей

        # считаем только "обычных" пользователей, без супер-юзеров
        if self.__class__ is User:
            User.count += 1

    # --- свойства ---

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        # логин менять нельзя
        print("Невозможно изменить логин!")

    @property
    def password(self):
        # пароль не показываем, только маску
        return "********"

    @password.setter
    def password(self, value):
        self._password = value

    # «левое» свойство grade, которое по условиям должно
    # писать сообщение и больше ничего не делать
    @property
    def grade(self):
        print("Неизвестное свойство grade")

    @grade.setter
    def grade(self, value):
        print("Неизвестное свойство grade")

    # --- методы сравнения по уровню (level) ---

    def __lt__(self, other):
        if isinstance(other, User):
            return self._level < other._level
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, User):
            return self._level > other._level
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, User):
            return self._level == other._level
        return NotImplemented

    # --- обычный метод ---

    def show_info(self):
        print(f"Name: {self._name}, Login: {self._login}")


class SuperUser(User):
    # атрибут класса — количество супер-пользователей
    count = 0

    def __init__(self, name: str, login: str, password: str, role: str, level: int):
        super().__init__(name, login, password, level)
        self._role = role
        SuperUser.count += 1

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    # show_info можно унаследовать как есть — формат совпадает
    # но можно и переопределить, если нужно что-то добавить
    # def show_info(self):
    #     super().show_info()

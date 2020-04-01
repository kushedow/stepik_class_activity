import time
from stepik_client import StepicClient


class StepikActivity:

    """ Активность студентов на Степике по ID класса и сопутствущие методы
    """

    def __init__(self, congig_id, config_secret):

        """Создаем объект, который будет рулить всеми запросами к API
        """

        self.client = StepicClient(congig_id, config_secret)

    def get_activity(self, student_id):

        """Возвращает список активности учащегося за последнюю неделю в решенных задачах по его id
        """

        student_activity_response = self.client.request("get",f"https://stepik.org/api/user-activities/+{student_id}")
        student_activity = student_activity_response.json().get("user-activities")[0]["pins"][:7]
        student_activity.reverse()
        return student_activity

    def get_studentname(self, student_id):

        """Возвращает имя студента по его id
        """

        student_profile = self.client.request("get",f"https://stepik.org:443/api/users/+{student_id}")
        full_name =  student_profile.json().get("users")[0].get("full_name")
        return full_name

    def get_students_in_class(self, class_id):

        """Получаем список студентов в группе
        """

        class_response = self.client.request("get", f"https://stepik.org/api/students?klass={class_id}&page=1")
        students_in_class = class_response.json().get("students", [])

        return students_in_class

    def get_activity_by_class(self, class_id):

        """Получаем активность студентов по номеру класса
        """

        students_in_class = self.get_students_in_class(class_id)

        for student in students_in_class:
            student_id = student["user"]
            student["activity"] = self.get_activity(student_id)
            student["full_name"] = self.get_studentname(student_id)
            time.sleep(1)

        return students_in_class
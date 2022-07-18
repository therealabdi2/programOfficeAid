from django.test import TestCase

from accounts.models import Programme, Department, Faculty
from courses.models import Course, CourseType, CourseCategory


class CourseTest(TestCase):

    def setUp(self):
        faculty = Faculty.objects.create(faculty_name='Test Faculty')
        department = Department.objects.create(department_name='Test Department', faculty=faculty)
        course_category = CourseCategory.objects.create(course_category_name='Test_category')
        course_type = CourseType.objects.create(course_type_name='Test_type',
                                                course_type_category=course_category,
                                                required_credits=21)
        programme = Programme.objects.create(degree_name='Test_program', department=department)

        self.course = Course.objects.create(
            course_name='Test 123',
            course_code='T123',
            course_details='This is a test course',
            course_credit=3,
            course_type=course_type,
            offered_in_semester=1
        )
        self.course.course_programme.set([programme])

    def test_course_listing(self):
        faculty = Faculty.objects.create(faculty_name='Test Faculty')
        department = Department.objects.create(department_name='Test Department', faculty=faculty)
        course_category = CourseCategory.objects.create(course_category_name='Test_category')
        course_type = CourseType.objects.create(course_type_name='Test_type',
                                                course_type_category=course_category,
                                                required_credits=21)

        self.assertEqual(f'{self.course.course_name}', 'Test 123')
        self.assertEqual(f'{self.course.course_code}', 'T123')
        self.assertEqual(f'{self.course.course_details}', 'This is a test course')
        self.assertEqual(f'{self.course.course_credit}', '3')
        self.assertEqual(f'{self.course.course_type}', course_type.course_type_name)
        self.assertEqual(self.course.course_programme.all()[0].degree_name, 'Test_program')
        self.assertEqual(f'{self.course.offered_in_semester}', '1')

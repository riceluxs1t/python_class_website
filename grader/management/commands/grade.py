from datetime import date

from django.core.management.base import BaseCommand
from django.db.models import ObjectDoesNotExist
from grader.models import Homework

from grader.config import GRADE_DIR


"""
A command that runs and grades homework submissions
"""


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('homework_name', type=str)
        parser.add_argument('user_name', type=str)

    def handle(self, *args, **options):

        homework_name = options.get('homework_name')
        user_name = options.get('user_name')

        if not homework_name or not user_name:
            print "You must supply the homework name and user name. i.e. python manage.py homework2 nate"
            exit(-1)

        grader = None

        print "Grading {0} for user {1} ... ".format(homework_name, user_name)

        # checks if the solution module exists
        try:
            grader = __import__("grader.solutions.%s" % homework_name, fromlist=['solutions'])
        except ImportError as e:
            print e
            print "The test cases must be set up for grading %s! try again later" % homework_name
            exit(-1)

        modules = []

        # refers to the Homework model and get all the expected modules from the student submission directory
        try:
            homework = Homework.objects.get(homework_name=homework_name)
            for function in homework.modules.split(','):
                modules.append(
                    __import__("grader.submissions.%s.%s.%s" % (homework_name, user_name, function), fromlist=['submissions'])
                )

            # run the test cases.
            score = grader.Grader(*modules).run_tests()

            # TODO: add a dimension

            self.write_grade(homework_name, user_name, score)

        except ObjectDoesNotExist:
            print "The corresponding project does not seem registered in the systems' Homework Model yet"

        except ImportError as e:
            print e
            print "Maybe a wrong file submitted"

        except SyntaxError as e:
            print e
            print "Some syntax in the submitted file? or an error in the judge system"

    # write the grade to the grade directory.
    def write_grade(self, project_name, user_name, score):
        print GRADE_DIR
        with open('%s/%s-%s.txt' % (GRADE_DIR, project_name, user_name), 'a+') as gradeFile:
            gradeFile.write("%s\t%s\t%s\n" % (user_name, score, date.today()))

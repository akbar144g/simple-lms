from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from courses.models import Course


class Command(BaseCommand):
    help = "Compare normal vs optimized query"

    def handle(self, *args, **kwargs):
        reset_queries()

        # N+1 Problem
        courses = Course.objects.all()
        for course in courses:
            print(course.instructor.username)

        normal_queries = len(connection.queries)

        reset_queries()

        # Optimized
        courses = Course.objects.for_listing()
        for course in courses:
            print(course.instructor.username)

        optimized_queries = len(connection.queries)

        self.stdout.write(f"N+1 Queries: {normal_queries}")
        self.stdout.write(f"Optimized Queries: {optimized_queries}")
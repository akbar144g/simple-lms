from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Prefetch


# ======================
# CATEGORY
# ======================
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    def __str__(self):
        return self.name


# ======================
# COURSE QUERYSET
# ======================
class CourseQuerySet(models.QuerySet):
    def for_listing(self):
        return self.select_related(
            "instructor",
            "category"
        ).prefetch_related(
            "lessons"
        )


# ======================
# COURSE
# ======================
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return self.title


# ======================
# LESSON
# ======================
class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# ======================
# ENROLLMENT QUERYSET
# ======================
class EnrollmentQuerySet(models.QuerySet):
    def for_student_dashboard(self):
        return self.select_related(
            "student",
            "course",
            "course__instructor"
        ).prefetch_related(
            "progress_set"
        )


# ======================
# ENROLLMENT
# ======================
class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    objects = EnrollmentQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course"
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


# ======================
# PROGRESS
# ======================
class Progress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}"
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Course, Lesson, Enrollment, Progress


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "category", "created_at")
    search_fields = ("title",)
    list_filter = ("category", "instructor")
    inlines = [LessonInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    search_fields = ("student__username", "course__title")
    list_filter = ("course",)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "lesson", "completed")
    list_filter = ("completed",)
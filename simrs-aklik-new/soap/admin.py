from django.contrib import admin


from .models import (
    Subjective,
    Objective,
    AssessmentICD10,
    AssessmentICD9,
    Planning
)


@admin.register(Subjective)
class SubjectiveAdmin(admin.ModelAdmin):
    pass


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    pass


@admin.register(AssessmentICD10)
class AssessmentICD10Admin(admin.ModelAdmin):
    pass


@admin.register(AssessmentICD9)
class AssessmentICD9Admin(admin.ModelAdmin):
    pass


@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    pass
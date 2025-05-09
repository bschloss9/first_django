'''
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
'''

from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Choice, Question


@admin.action(description="Export selected questions to CSV")
def export_questions_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="questions.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Question Text", "Published Date"])  # CSV header

    for question in queryset:
        writer.writerow([question.id, question.question_text, question.pub_date])

    return response

@admin.action(description="Export selected poll results (one line per question)")
def export_poll_results_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="poll_results_flat.csv"'

    writer = csv.writer(response)
    
    # Write the header — dynamic based on max number of choices
    max_choices = max((q.choice_set.count() for q in queryset), default=0)
    header = ["Question ID", "Question Text"]
    for i in range(1, max_choices + 1):
        header.extend([f"Choice {i}", f"Votes {i}"])
    writer.writerow(header)

    # Write each question and its choices on one row
    for question in queryset:
        row = [question.id, question.question_text]
        for choice in question.choice_set.all():
            row.extend([choice.choice_text, choice.votes])
        writer.writerow(row)

    return response



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    actions = [export_questions_csv]  
    actions = [export_questions_csv, export_poll_results_csv]



admin.site.register(Question, QuestionAdmin)

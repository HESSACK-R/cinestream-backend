# migrate_view.py
from django.http import JsonResponse
from django.core.management import call_command

def run_migrations(request):
    try:
        call_command("migrate")
        return JsonResponse({"status": "success", "message": "Migrations applied successfully"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

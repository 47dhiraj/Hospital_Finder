from django.core.management.base import BaseCommand
from django.core import management
from django.apps import apps
import os



class Command(BaseCommand):
    
    help = "Dump all models in the app into separate UTF-8 JSON fixture files"

    def handle(self, *args, **kwargs):

        app_label = "app"                       # change if your app name is different

        # Get all models from the app
        models = apps.get_app_config(app_label).get_models()

        # Ensure fixtures folder exists
        fixtures_path = os.path.join(app_label, "fixtures")
        os.makedirs(fixtures_path, exist_ok=True)

        for model in models:
            model_name = model.__name__
            file_path = os.path.join(fixtures_path, f"{model_name}.json")

            self.stdout.write(f"📦 Dumping {model_name} → {file_path}")

            with open(file_path, "w", encoding="utf-8") as f:
                management.call_command(
                    "dumpdata",
                    f"{app_label}.{model_name}",
                    indent=4,
                    stdout=f
                )

        self.stdout.write(self.style.SUCCESS("🔥 All models dumped successfully in UTF-8!"))



# from django.core.management.base import BaseCommand
# from django.core import management


# class Command(BaseCommand):

#     def handle(self, *args, **kwargs):
        
#         with open("app/fixtures/Surg.json", "w", encoding="utf-8") as f:
#             management.call_command(
#                 "dumpdata",
#                 "app.Surg",
#                 indent=4,
#                 stdout=f
#             )

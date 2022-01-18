import shutil
from subprocess import call
from django.core.management.base import BaseCommand

PROJECT_PATH = r"/Users/temporaryadmin/projects/django-blog/myblog/"


class Command(BaseCommand):
    help = "Check Python files for PEP8 compliance"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            dest="fix",
            default=False,
            help="Whether to also attempt to fix files",
        )

    def handle(self, *args, **options):
        self.stdout.write("Linting Python code...")
        shutil.os.chdir(PROJECT_PATH)
        if options["fix"]:
            call(["black", "--line-length", "79", "."])
        flake_return_value = call(
            [
                "flake8",
                "--extend-ignore",
                "E203,E501",
                "--exclude",
                "node_modules/*,venv/*,.direnv/*,configuration.py",
                "./",
            ]
        )
        if flake_return_value > 0:
            exit(flake_return_value)
        black_return_value = call(
            ["black", "--line-length", "79", ".", "--check"]
        )
        if black_return_value > 0:
            exit(black_return_value)

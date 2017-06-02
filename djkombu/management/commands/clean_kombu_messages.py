from __future__ import absolute_import

from django.core.management.base import BaseCommand

from ...models import Message


def pluralize(desc, value):
    if value > 1:
        return desc + 's'
    return desc


class Command(BaseCommand):
    requires_model_validation = True

    def handle(self, *args, **options):
        count = Message.objects.filter(visible=False).count()

        print('Removing {0} invisible {1} from database... '.format(
            count, pluralize('message', count)))
        Message.objects.cleanup()

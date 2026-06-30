from django.db import transaction


class BaseService:

    model = None

    @classmethod
    @transaction.atomic
    def create(cls, validated_data):
        return cls.model.objects.create(**validated_data)

    @classmethod
    @transaction.atomic
    def update(cls, instance, validated_data):

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def soft_delete(cls, instance):

        instance.is_deleted = True

        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def restore(cls, instance):

        instance.is_deleted = False

        instance.save()

        return instance

    @classmethod
    def get_deleted(cls, pk):

        return cls.model.objects.filter(
            id=pk,
            is_deleted=True
        ).first()
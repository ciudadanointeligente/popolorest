from rest_framework import serializers
from popolo.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id',
                  'name',
                  'family_name',
                  'given_name',
                  'additional_name',
                  'honorific_prefix',
                  'honorific_suffix',
                  'patronymic_name',
                  'sort_name',
                  'email',
                  'gender',
                  'birth_date',
                  'death_date',
                  'image',
                  'summary',
                  'biography',
                  'national_identity')

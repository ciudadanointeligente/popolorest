from rest_framework import serializers
from popolo.models import Person, ContactDetail, Membership


class ContactDetailSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='contact_type')

    class Meta:
        model = ContactDetail
        fields = ('id', 'value', 'label', 'type')


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership


class ContactDetailedRelatedField(serializers.RelatedField):
    queryset = ContactDetail.objects.all()

    def to_representation(self, value):
        if isinstance(value, ContactDetail):
            serializer = ContactDetailSerializer(value)
            return serializer.data

class MembershipRelatedField(serializers.RelatedField):
    queryset = Membership.objects.all()

    def to_representation(self, value):
        if isinstance(value, Membership):
            serializer = MembershipSerializer(value)
            return serializer.data


class PersonSerializer(serializers.ModelSerializer):
    contact_details = ContactDetailedRelatedField(many=True)
    memberships = MembershipRelatedField(many=True)

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
                  'national_identity',
                  'contact_details',
                  'memberships',)

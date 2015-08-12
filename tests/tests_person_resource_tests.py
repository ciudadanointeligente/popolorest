
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_popolorest
------------
Tests for `popolorest` models module.
"""

from django.test import TestCase
from popolo.models import Person, ContactDetail, Organization
from popolorest.serializers import PersonSerializer, MembershipSerializer
import json
from rest_framework.status import is_success


class PersonSerializerTestCase(TestCase):
    def setUp(self):
        pass

    def test_serialize_person(self):
        person = Person.objects.create(name=u'Rita Levi-Montalcini')
        person.add_contact_detail(contact_type=ContactDetail.CONTACT_TYPES.email,
                                  value='rita@example.com',
                                  label='email')
        serializer = PersonSerializer(person)
        self.assertEquals(serializer.data['name'], person.name)
        self.assertIn('contact_details', serializer.data.keys())
        self.assertEquals(len(serializer.data['contact_details']), 1)
        self.assertEquals(serializer.data['contact_details'][0]['value'], 'rita@example.com')
        self.assertEquals(serializer.data['contact_details'][0]['label'], 'email')
        self.assertEquals(serializer.data['contact_details'][0]['type'], ContactDetail.CONTACT_TYPES.email)

    def test_get_the_persons_resource(self):
        person = Person.objects.create(name=u'Rita Levi-Montalcini')
        url = '/persons/'
        response = self.client.get(url)
        self.assertTrue(is_success(response.status_code))
        response_object = json.loads(response.content.decode())
        self.assertIn('total', response_object.keys())
        self.assertIn('page', response_object.keys())
        self.assertIn('per_page', response_object.keys())
        self.assertIn('has_more', response_object.keys())
        self.assertIn('next_url', response_object.keys())
        self.assertIn('result', response_object.keys())
        self.assertEquals(response_object['result'][0]['name'], person.name)

class MembershipSerializerTestCase(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name=u'Rita Levi-Montalcini')
        self.organization = Organization.objects.create(name=u"Scientists")
        self.person.add_membership(self.organization)
        self.membership = self.person.memberships.first()
        self.membership.start_date = "2005-05-06"
        self.membership.end_date=None
        self.membership.label="Rita is a scientist"
        self.membership.save()

    def test_serializer_initialization(self):
        serializer = MembershipSerializer(self.membership)
        data = serializer.data
        self.assertEquals(data['start_date'], self.membership.start_date)
        self.assertIsNone(data['end_date'])
        self.assertEquals(data['label'], self.membership.label)

    def test_membership_in_person_serializer(self):
        serializer = PersonSerializer(self.person)
        self.assertIn('memberships', serializer.data.keys())
        self.assertEquals(len(serializer.data['memberships']), 1)
        self.assertEquals(serializer.data['memberships'][0]['start_date'], self.membership.start_date)
        self.assertIsNone(serializer.data['memberships'][0]['end_date'])
        self.assertEquals(serializer.data['memberships'][0]['label'], self.membership.label)


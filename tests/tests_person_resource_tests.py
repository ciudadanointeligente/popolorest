
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_popolorest
------------
Tests for `popolorest` models module.
"""

from django.test import TestCase
from popolo.models import Person, ContactDetail
from popolorest.serializers import PersonSerializer
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
        response_object = json.loads(response.content)
        self.assertIn('total', response_object.keys())
        self.assertIn('page', response_object.keys())
        self.assertIn('per_page', response_object.keys())
        self.assertIn('has_more', response_object.keys())
        self.assertIn('next_url', response_object.keys())
        self.assertIn('result', response_object.keys())
        self.assertEquals(response_object['result'][0]['name'], person.name)

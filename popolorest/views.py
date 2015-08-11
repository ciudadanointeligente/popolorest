__author__ = 'guglielmo'
from popolo.models import Person, Organization, Membership, Post
from rest_framework import viewsets
from popolorest.serializers import PersonSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.compat import OrderedDict
# ViewSets define the view behavior.


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'per_page'
    max_page_size = 30

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next_url', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('has_more', self.get_next_link() is not None),
            ('page', self.page.number),
            ('per_page', self.page_size),
            ('result', data)
        ]))


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, )
    pagination_class = LargeResultsSetPagination


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

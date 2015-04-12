# -*- coding: utf-8 -*-
""" Carpooling API implemented using Google Cloud Endpoints on Google App Engine
"""

import endpoints
from protorpc import remote
from google.appengine.ext import ndb

from models import RunRequest
from models import RunOffer

from geopy import geocoders

package = 'Carpooling'


@endpoints.api(name='carpooling', version='v1')
class CarpoolingApi (remote.Service):

    @RunRequest.method(path='request', http_method='POST',
                       name='runrequest.insert')
    def RunRequestInsert(self, run_request):
        geocoder = geocoders.Nominatim()

        location = geocoder.geocode(run_request.fromAddress)

        if location is None:
            raise endpoints.BadRequestException(
                "L'adresse de depart est invalide")

        run_request.fromCoord = ndb.GeoPt(location.latitude, location.longitude)

        location = geocoder.geocode(run_request.toAddress)

        if location is None:
            raise endpoints.BadRequestException(
                "L'adresse de destination est invalide")

        run_request.toCoord = ndb.GeoPt(location.latitude, location.longitude)

        run_request.put()
        return run_request

    @RunRequest.query_method(path='requests', name='runrequest.list')
    def RunRequestList(self, query):
        return query

    @RunOffer.method(path='offers', http_method='POST',
                     name='runoffer.insert')
    def RunOfferInsert(self, run_offer):
        geocoder = geocoders.Nominatim()

        location = geocoder.geocode(run_offer.fromAddress)

        if location is None:
            raise endpoints.BadRequestException(
                "L'adresse de depart est invalide")

        run_offer.fromCoord = ndb.GeoPt(location.latitude, location.longitude)

        location = geocoder.geocode(run_offer.toAddress)

        if location is None:
            raise endpoints.BadRequestException(
                "L'adresse de destination est invalide")

        run_offer.toCoord = ndb.GeoPt(location.latitude, location.longitude)

        run_offer.put()
        return run_offer

    @RunOffer.query_method(path='offer', name='runoffer.list')
    def RunOfferList(self, query):
        return query

APPLICATION = endpoints.api_server([CarpoolingApi], restricted=False)
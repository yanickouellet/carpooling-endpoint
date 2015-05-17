# -*- coding: utf-8 -*-
""" Carpooling API implemented using Google Cloud Endpoints on Google App Engine
"""

import endpoints
from protorpc import remote
from google.appengine.ext import ndb

from models import RunRequest
from models import RunOffer
from models import Match

from geopy import geocoders
from geopy.distance import vincenty

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

        run_request.matched = False

        run_request.put()

        self.TryToMatchRequest(run_request)

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

        run_offer.remainingPlaces = run_offer.places

        run_offer.put()

        self.TryToMatchOffer(run_offer)

        return run_offer

    @RunOffer.query_method(path='offer', name='runoffer.list')
    def RunOfferList(self, query):
        return query

    @Match.query_method(path='matches', name='match.list')
    def MatchList(self, query):
        return query

    def TryToMatchOffer(self, offer):
        requests = RunRequest.query(RunRequest.matched == False)

        for request in requests:
            fromDist = self.ComputeDist(request.fromCoord, offer.fromCoord)
            toDist = self.ComputeDist(request.toCoord, offer.toCoord)

            if (fromDist + toDist)  <= offer.kmValue * 1000:
                self.MakeMatch(request, offer)

                if(offer.remainingPlaces == 0):
                    break


    def TryToMatchRequest(self, request):
        offers = RunOffer.query(RunOffer.remainingPlaces >= 1)

        for offer in offers:
            fromDist = self.ComputeDist(request.fromCoord, offer.fromCoord)
            toDist = self.ComputeDist(request.toCoord, offer.toCoord)

            if (fromDist + toDist)  <= offer.kmValue * 1000:
                self.MakeMatch(request, offer)
                break

    def MakeMatch(self, request, offer):
        match = Match(request=request.key, offer=offer.key)
        match.put()

        request.matched = True
        request.put()

        offer.remainingPlaces -= 1
        offer.put()

    def ComputeDist(self, a, b):
        return vincenty((a.lat, a.lon), (b.lat, b.lon)).meters


APPLICATION = endpoints.api_server([CarpoolingApi], restricted=False)
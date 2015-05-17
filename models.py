from google.appengine.ext import ndb

from endpoints_proto_datastore.ndb import EndpointsModel


class RunRequest(EndpointsModel):
    fromAddress = ndb.StringProperty()
    toAddress = ndb.StringProperty()
    hour = ndb.IntegerProperty()
    minute = ndb.IntegerProperty()
    dayOfWeek = ndb.IntegerProperty()
    date = ndb.DateProperty()
    ponctual = ndb.BooleanProperty()
    matched = ndb.BooleanProperty()

    fromCoord = ndb.GeoPtProperty()
    toCoord = ndb.GeoPtProperty()


class RunOffer(EndpointsModel):
    fromAddress = ndb.StringProperty()
    toAddress = ndb.StringProperty()
    hour = ndb.IntegerProperty()
    minute = ndb.IntegerProperty()
    dayOfWeek = ndb.IntegerProperty()
    date = ndb.DateProperty()
    ponctual = ndb.BooleanProperty()
    places = ndb.IntegerProperty()
    remainingPlaces = ndb.IntegerProperty()
    kmValue = ndb.IntegerProperty()

    fromCoord = ndb.GeoPtProperty()
    toCoord = ndb.GeoPtProperty()


class Match(EndpointsModel):
    request = ndb.KeyProperty(kind=RunRequest)
    offer = ndb.KeyProperty(kind=RunOffer)

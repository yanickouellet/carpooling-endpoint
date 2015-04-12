from google.appengine.ext import ndb

from endpoints_proto_datastore.ndb import EndpointsModel


class RunRequest(EndpointsModel):
    fromAddress = ndb.StringProperty()
    toAddress = ndb.StringProperty()
    hour = ndb.IntegerProperty()
    minute = ndb.IntegerProperty()
    dayOfWeek = ndb.IntegerProperty()
    date = ndb.DateTimeProperty()
    ponctual = ndb.BooleanProperty()

    fromCoord = ndb.GeoPtProperty()
    toCoord = ndb.GeoPtProperty()


class RunOffer(EndpointsModel):
    fromAddress = ndb.StringProperty()
    toAddress = ndb.StringProperty()
    hour = ndb.IntegerProperty()
    minute = ndb.IntegerProperty()
    dayOfWeek = ndb.IntegerProperty()
    date = ndb.DateTimeProperty()
    ponctual = ndb.BooleanProperty()
    places = ndb.IntegerProperty()
    kmValue = ndb.IntegerProperty()

    fromCoord = ndb.GeoPtProperty()
    toCoord = ndb.GeoPtProperty()

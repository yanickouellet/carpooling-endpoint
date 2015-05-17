from google.appengine.ext import ndb

from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsAliasProperty

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

    user = ndb.UserProperty()
    match = ndb.KeyProperty(kind='RunOffer')

    @EndpointsAliasProperty()
    def driver(self):
        if self.match is not None:
            return self.match.get().user.email()
        return ''


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

    user = ndb.UserProperty()
    matches = ndb.KeyProperty(kind=RunRequest, repeated=True)

    def passengerSet(self, value):
        pass

    @EndpointsAliasProperty(setter=passengerSet, repeated=True)
    def passengers(self):
        list = []
        for key in self.matches:
            list.append(key.get().user.email())
        return list

class Match(EndpointsModel):
    request = ndb.KeyProperty(kind=RunRequest)
    offer = ndb.KeyProperty(kind=RunOffer)

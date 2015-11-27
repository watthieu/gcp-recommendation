class Accommodation(ndb.Model):
  title   = ndb.StringProperty(required=True)
  picture = ndb.StringProperty()
  price   = ndb.IntegerProperty()
  rooms   = ndb.IntegerProperty()
  rating  = ndb.FloatProperty()
  type    = ndb.StringProperty()

class Rating(ndb.Model):
  userName  = ndb.StringProperty(required=True)
  accoTitle = ndb.StringProperty(required=True)
  accoAttrs = ndb.JsonProperty()
  rating    = ndb.FloatProperty()

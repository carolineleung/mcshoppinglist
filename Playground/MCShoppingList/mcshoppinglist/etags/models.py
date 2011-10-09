from mongoengine.document import Document
from mongoengine.fields import DateTimeField, StringField
from mcshoppinglist.shared.models.constants import DEFAULT_DATE

class EtagCacheEntry(Document):
    #  str(bson.ObjectId) i.e. the string hex value of the model's mongoengine/mongodb ObjectId. Note that mongoengine Document.id is a bson.ObjectId instance; call str on it.
    target_model_id = StringField(min_length=1)
    target_category = StringField(max_length=200)
    # TODO Add an index on etag
    etag = StringField(max_length=200)
    last_modified = DateTimeField(default=DEFAULT_DATE)


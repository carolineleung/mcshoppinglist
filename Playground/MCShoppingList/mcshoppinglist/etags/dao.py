from mcshoppinglist.etags.models import EtagCacheEntry
from mcshoppinglist.shared.dao.daobase import  DaoBase

class EtagCacheEntryDao(DaoBase):
    def create_etag_cache_entry(self):
        return EtagCacheEntry()

    def get_by_id(self, id):
        return self.get_by_id_from_objects(id, EtagCacheEntry.objects)

    def get_by_target(self, target_model_id, target_category):
        id = str(target_model_id)
        return EtagCacheEntry.objects.filter(target_model_id=id, target_category=target_category)

    def get_by_etag(self, etag):
        return EtagCacheEntry.objects.filter(etag__exact=etag)


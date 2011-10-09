from datetime import datetime
from mcshoppinglist.shared.models.constants import ModelStateConstants, DEFAULT_STATE

class DaoBase(object):
    def delete(self, model):
        model.state = ModelStateConstants.DELETED
        self.save(model)

    def save(self, model):
        # TODO Consider making this optional (since it prevents explicitly setting model.last_modified elsewhere).
        if hasattr(model, 'last_modified'):
            model.last_modified = datetime.utcnow()
        model.save()

    def get_by_id_from_objects(self, id, model_objects):
        """
        model_objects: ShoppingListItem.objects
        """
        model = None
        try:
            # TODO can we use Document.objects(id=objid) to avoid the exception handling? get() raises DoesNotExist.
            # Auto wrapped if id is already an ObjectId. Auto converted to ObjectId if id is hex string.
            model = model_objects.get(id=id)
            # TODO Handle list return value
        except Exception:
            # ignore
            pass
        return model

def fix_state(model):
    if not hasattr(model, 'state') or not model.state in ModelStateConstants.ALL_STATES:
        model.state = DEFAULT_STATE


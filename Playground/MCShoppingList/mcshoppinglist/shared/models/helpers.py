from mcshoppinglist.shared.exceptions import ShoppingListError

def get_id_str(doc):
    """
    Avoid using MongoEngine Document self.id which returns an instance of ObjectId
    and if converted to a str uses repr: ObjectId('4d7d0785cf66075114000002')
    Instead, this returns the hash string '4d7d0785cf66075114000002' via str().
    """
    if not hasattr(doc, 'id'):
        raise ShoppingListError('No id property found for doc: {0}'.format(doc))
    id = str(doc.id)
    if not id:
        raise ShoppingListError('Missing id for doc: {0}'.format(doc))
    return id

import shoppinglists

class TypeResolver:
    def resolve(self, class_name):
        """
        returns: a type (classobj) for the class_name, or raises exception.
        """
        raise TypeError('Unable to resolve type: %s' % class_name)

class SpecifiedTypeResolver(TypeResolver):
    def __init__(self, types_dict):
        """
        types_dict: map of class_name to type (classobj), e.g. globals().
        Note globals() is module scope (won't include scope from other modules).
        """
        self.types_dict = types_dict
        
    def resolve(self, class_name):
        type = None
        if class_name in self.types_dict:
            type = self.types_dict[class_name]
        if not type:
            return TypeResolver.resolve(self, class_name)
        return type

class ShoppingListTypeResolver(TypeResolver):
    # TODO Is there a more flexible/dynamic way of getting the modules in this django project?
    SHOPPING_LIST_MODULES = [shoppinglists.api, shoppinglists.models]

    def __init__(self, modules_to_search=SHOPPING_LIST_MODULES):
        self._modules = modules_to_search

    def add_modules_to_search(self, modules):
        if not self._modules:
            self._modules = []
        self._modules.extend(modules)

    def resolve(self, class_name):
        modules = self._modules
        type = None
        for module in modules:
            type = getattr(module, class_name)
            if type:
                break
        if not type:
            return TypeResolver.resolve(self, class_name)
        return type
  
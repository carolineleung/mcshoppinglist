from datetime import datetime
from django.db import models
from shoppinglists.models import ShoppingListItem, ShoppingList

# Avoid null dates.
DEFAULT_DATE=datetime(2011, 01, 01)

# TODO Get the etagmanager out of shoppinglists.models.py

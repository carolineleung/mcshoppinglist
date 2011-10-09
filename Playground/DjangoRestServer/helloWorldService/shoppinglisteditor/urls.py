from django.conf.urls.defaults import patterns

urlpatterns = patterns('shoppinglisteditor.views',
    (r'^$', 'shopping_list_editor'),
    (r'^editor2/?$', 'shopping_list_editor2'),
)
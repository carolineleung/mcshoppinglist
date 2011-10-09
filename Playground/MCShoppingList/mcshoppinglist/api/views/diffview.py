import re
from mcshoppinglist.api.views.helpers import ViewRequestHelper, ViewResponseHelper
from mcshoppinglist.api.views.listview import ShoppingListView
from mcshoppinglist.etags.dao import EtagCacheEntryDao
from mcshoppinglist.etags.etagmanager import EtagManager
from mcshoppinglist.shared.logfactory import LogFactory

logger = LogFactory.get_logger(__name__)

class ShoppingListDiffView(object):
    def __init__(self):
        self.req_helper = ViewRequestHelper()
        self.resp_helper = ViewResponseHelper()

    def _get_etag_from_request(self, request):
        etag = None
        try:
            #if_none_match_key = 'HTTP_IF_NONE_MATCH' # Django converts If-None-Match to uppercase with _
            if_none_match_key = 'If-None-Match' # Django converts If-None-Match to uppercase with _
            if if_none_match_key in request.headers:
                # TODO Can we make key lookup case insensitive?
                request_etags = request.headers[if_none_match_key]
                if request_etags:
                    # http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
                    # If-None-Match: "xyzzy", "r2d2xxxx", "c3piozzzz"

                    # Take the first etag in list. Client should not be sending multiple.
                    split_etags = request_etags.split(',')
                    if split_etags and len(split_etags) > 0 and split_etags[0] and len(split_etags[0]) > 0:
                        # split_etags[0] = '"xyzzy" '
                        # Remove the quotes and whitespace
                        etag = re.sub(r'^\s*"+', '', split_etags[0])
                        etag = re.sub(r'"+\s*$', '', etag)
                        # etag = 'xyzzy'
        except Exception as ex:
            logger.error('Failed to parse ETag from request. Cause: {0}'.format(ex))
        return etag

    def _shopping_list_diff_get(self, request, list_id):
        since_last_modified = None
        # ETag parsing errors should not be fatal to the request.
        try:
            request_etag = self._get_etag_from_request(request)
            if request_etag and len(request_etag) > 0:
                logger.debug('Got ETag from request: {0}'.format(request_etag))
                etag_queryset = EtagCacheEntryDao().get_by_etag(request_etag)
                if etag_queryset and etag_queryset.count() > 0:
                    logger.debug('ETag matched. Not modified. {0}'.format(request_etag))
                    response = self.resp_helper.create_response_not_modified()
                    # Include the matched etag per http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
                    response.headers['ETag'] = request_etag
                    # TODO Include other cache headers
                    return response
                else:
                    logger.debug('ETag not matched. Extracting last_modified. {0}'.format(request_etag))
                    try:
                        since_last_modified = EtagManager().get_last_modified_from_etag(request_etag)
                        logger.debug('ETag not matched. {0}  since_last_modified: {1}'.format(request_etag, since_last_modified))
                    except Exception as ex2:
                        logger.info('Non-fatal error. Failed to parse request header ETag: {0}  Cause: {1}'.format(
                            request_etag, ex2.message), exc_info=1)
            # else:
            # TODO else Handle If-Modified-Since. Per http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
            # "If none of the entity tags match, then the server MAY perform the requested method as if the If-None-Match header field did not exist, but MUST also ignore any If-Modified-Since header field(s) in the request. That is, if no entity tags match, then the server MUST NOT return a 304 (Not Modified) response."
        except Exception as ex:
            logger.warn('Failed to process request header ETag. Cause: {0}'.format(ex), exc_info=1)

        list_view = ShoppingListView()
        return list_view.get_shopping_list_detail(list_id, since_last_modified=since_last_modified,
                                         include_deleted_items=True, include_etag_headers=True)

    def shopping_list_diff_handler(self, request):
        list_id = self.req_helper.get_list_id(request)
        if request.method == 'GET':
            return self._shopping_list_diff_get(request, list_id)
        # 405 per http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        return self.resp_helper.create_response_not_allowed(['GET'])

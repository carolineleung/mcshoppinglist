package com.mcshoppinglist.app.json;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.StatusLine;

import com.google.gson.Gson;
import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.json.model.ErrorResponse;
import com.mcshoppinglist.app.json.model.IJsonSerializable;
import com.mcshoppinglist.app.json.model.ResponseContainer;
import com.mcshoppinglist.app.json.model.ShoppingList;
import com.mcshoppinglist.app.json.model.ShoppingListItem;
import com.mcshoppinglist.app.json.model.UpdateRequest;
import com.mcshoppinglist.app.json.model.UpdateResponse;
import com.mcshoppinglist.app.network.HttpRequester;
import com.mcshoppinglist.app.network.HttpRequester.HttpRequestType;
import com.mcshoppinglist.app.util.MCLogger;

public class JsonParser {

    // TODO set up all the URLs
    // private static final String SERVER_BASE_URL = "http://192.168.11.196:888/api/v1/shoppinglists/";
    private static final String SERVER_HOST = "64.62.188.245"; // m1.xen.prgmr.com";

    // private static final int SERVER_PORT = 888; // "Production"
    private static final int SERVER_PORT = 889; // "Development"
    private static final String SERVER_BASE_URL = "http://" + SERVER_HOST + ":" + SERVER_PORT
                    + "/api/v1/shoppinglists/";
    private static final String PUSH_ITEMS_DIFFS_RESOURCE_URL = "/items/";
    private static final String GET_ITEMS_DIFFS_RESOURCE_URL = "/diff/";

    private final HttpRequester httpRequestHandler;
    private final Gson gson;

    public JsonParser() {
        httpRequestHandler = new HttpRequester();
        gson = new Gson();
    }

    public ResponseContainer<ShoppingList> getShoppingList(String shoppingListId) {
        ResponseContainer<ShoppingList> responseContainer = executeRequest(ShoppingList.class,
                        HttpRequestType.Get, getShoppingListResourceUrl(shoppingListId), null, null);
        return responseContainer;
    }

    public boolean updateItem(String shoppingListId, ShoppingListItem item, String currEtag) {
        UpdateRequest updateRequest = new UpdateRequest();
        List<ShoppingListItem> itemAsList = new ArrayList<ShoppingListItem>();
        itemAsList.add(item);
        updateRequest.setAction(UpdateRequest.ACTION_UPDATE);
        updateRequest.setItems(itemAsList);

        ResponseContainer<UpdateResponse> responseContainer = executeRequest(UpdateResponse.class,
                        HttpRequestType.Post, getPushItemDiffResourceUrl(shoppingListId),
                        updateRequest, currEtag);

        UpdateResponse updateResponse = responseContainer.getObject();
        if (updateResponse == null) {
            ErrorResponse errorResponse = responseContainer.getErrorResponse();
            MCLogger.w(getClass(), "Error updating item id="
                            + item.getId()
                            + (errorResponse != null ? ", msg=" + errorResponse.getErrorMessage()
                                            : ""));
        }
        return updateResponse != null;
    }

    public ResponseContainer<ShoppingList> getItemDiffs(String shoppingListId, String currEtag) {
        String retrieveItemDiffsUrl = getRetrieveItemDiffResourceUrl(shoppingListId);
        ResponseContainer<ShoppingList> responseContainer = executeRequest(ShoppingList.class,
                        HttpRequestType.Get, retrieveItemDiffsUrl, null, currEtag);
        return responseContainer;

    }

    private <T> ResponseContainer<T> executeRequest(Class<T> classOfT, HttpRequestType type,
                    String url, IJsonSerializable sourceJson, String etagHeader) {
        ResponseContainer<T> responseContainer = new ResponseContainer<T>();
        try {
            HttpResponse response = httpRequestHandler.executeRequest(type, url, sourceJson,
                            etagHeader);
            if (response == null) {
                MCLogger.e(getClass(), "Null http response from executeRequest, url=" + url
                                + ", class=" + classOfT.getSimpleName());
            } else {
                StatusLine statusLine = response.getStatusLine();
                int statusCode = statusLine.getStatusCode();
                HttpEntity responseEntity = response.getEntity();

                if (responseEntity == null) {
                    if (statusCode != HttpStatus.SC_NOT_MODIFIED) {
                        MCLogger.e(getClass(),
                                        "Null responseEntity from executeRequest, statusCode="
                                                        + statusCode + ", url=" + url + ", class="
                                                        + classOfT.getSimpleName());
                    }
                } else {
                    InputStream content = responseEntity.getContent();
                    Reader reader = new InputStreamReader(content);

                    if (statusCode != HttpStatus.SC_OK) {
                        // Request fails
                        String responseStr = statusLine.getReasonPhrase();
                        MCLogger.w(getClass(), "Error statusCode=" + statusCode + ", responseStr="
                                        + responseStr + " for URL=" + url);

                        ErrorResponse errorResponse = gson.fromJson(reader, ErrorResponse.class);
                        responseContainer.setErrorResponse(errorResponse);

                    } else {
                        // Request succeeds
                        Header[] eTagHeaders = response.getHeaders(AppConstants.HTTP_HEADER_ETAG);
                        if (eTagHeaders != null && eTagHeaders.length > 0) {
                            String etag = eTagHeaders[0].getValue(); // TODO verify if can just use first one's value
                            responseContainer.setETag(etag);
                        }
                        responseContainer.setObject(gson.fromJson(reader, classOfT));
                    }
                }
            }
        } catch (Exception e) {
            MCLogger.w(getClass(), "Unexpected exception for URL: " + url, e);

        }

        return responseContainer;
    }

    private String getShoppingListResourceUrl(String shoppingListId) {
        return SERVER_BASE_URL + shoppingListId + "/";
    }

    private String getRetrieveItemDiffResourceUrl(String shoppingListId) {
        return SERVER_BASE_URL + shoppingListId + GET_ITEMS_DIFFS_RESOURCE_URL;
    }

    private String getPushItemDiffResourceUrl(String shoppingListId) {
        return SERVER_BASE_URL + shoppingListId + PUSH_ITEMS_DIFFS_RESOURCE_URL;
    }

}

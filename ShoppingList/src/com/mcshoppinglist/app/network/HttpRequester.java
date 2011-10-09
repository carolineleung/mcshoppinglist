package com.mcshoppinglist.app.network;

import java.io.IOException;
import java.io.UnsupportedEncodingException;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpEntityEnclosingRequestBase;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.protocol.HTTP;

import com.google.gson.Gson;
import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.json.model.IJsonSerializable;
import com.mcshoppinglist.app.util.MCLogger;

public class HttpRequester {

    private HttpParams httpParams;

    public enum HttpRequestType {
        Get, Put, Post, Delete;
    }

    /**
     * Execute the HTTP request based on the given type and URL.
     * 
     * @param type
     * @param url
     * @param sourceJson
     *            Source Json object to send over the wire, for Post/Put requests only
     * @throws IOException
     * @throws ClientProtocolException
     */
    public HttpResponse executeRequest(HttpRequestType type, String url,
                    IJsonSerializable sourceJson, String eTagHeader) {

        DefaultHttpClient httpClient = new DefaultHttpClient(getHttpParams());
        HttpUriRequest request = createHttpRequest(type, url);
        if (request == null) {
            MCLogger.e(getClass(), "Ignored unsupported request type " + type + ", url=" + url);
            return null;
        }
        HttpResponse response = null;
        try {
            setHeaders(request, eTagHeader);
            // Only for HttpPost and HttpPut
            setParameters(type, request, sourceJson);

            response = httpClient.execute(request);

        } catch (Exception e) {
            request.abort();
            MCLogger.e(getClass(), "Exception in executeResponse " + type + ", url=" + url, e);
        }
        return response;
    }

    // TODO cl: verify we can reuse the httpParams for multiple requests
    private HttpParams getHttpParams() {
        if (httpParams == null) {
            httpParams = new BasicHttpParams();
            HttpConnectionParams.setConnectionTimeout(httpParams,
                            AppConstants.CONNECTION_TIMEOUT_MILLIS);
            HttpConnectionParams.setSoTimeout(httpParams, AppConstants.SOCKET_TIMEOUT_MILLIS);
        }
        return httpParams;
    }

    private HttpUriRequest createHttpRequest(HttpRequestType type, String url) {
        HttpUriRequest request = null;
        switch (type) {
        case Get:
            request = new HttpGet(url);
            break;
        case Post:
            request = new HttpPost(url);
            break;
        case Put:
            request = new HttpPut(url);
            break;
        case Delete:
            request = new HttpDelete(url);
            break;
        }
        return request;
    }

    private void setParameters(HttpRequestType type, HttpUriRequest request,
                    IJsonSerializable sourceJson) throws UnsupportedEncodingException {
        if (sourceJson != null && (type == HttpRequestType.Post || type == HttpRequestType.Put)) {
            Gson gson = new Gson();
            String jsonStr = gson.toJson(sourceJson);
            ((HttpEntityEnclosingRequestBase) request).setEntity(new StringEntity(jsonStr,
                            HTTP.UTF_8));
        }
    }

    private void setHeaders(HttpUriRequest request, String etag) {
        if (etag != null) {
            // request.setHeader(AppConstants.HTTP_HEADER_ETAG, etag);
            request.setHeader(AppConstants.HTTP_HEADER_IF_NONE_MATCH, etag);
        }
    }

    // public interface IHttpRequestListener<T> {
    // void onSuccess(T result);
    // void onFailure(StatusLine responseStatus); // TODO need to parse response for error statusCode?
    // void onException(Exception e);
    //
    // }

}

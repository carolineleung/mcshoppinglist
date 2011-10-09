package com.mcshoppinglist.app.json.model;

import java.util.ArrayList;
import java.util.Collection;

/*
 * Declaring this class so we can have a list impl that implements <code>IJsonSerializable</code>, for additional
 * type-safety (used in JsonParser.executeRequest)
 */
public class JsonList<E> extends ArrayList<E> implements IJsonSerializable {

    private static final long serialVersionUID = -6334550769205428580L;

    public JsonList() {
        super();
    }

    public JsonList(Collection<? extends E> collection) {
        super(collection);
    }

    public JsonList(int capacity) {
        super(capacity);
    }

}

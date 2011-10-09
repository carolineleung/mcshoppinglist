package com.mcshoppinglist.app.json.model;

import com.google.gson.annotations.SerializedName;

public class ShoppingListItem implements IJsonSerializable {

    private String id;

    private String name;

    private String labels;

    private boolean checked;

    private int position;

    @SerializedName("additional_items")
    private String additionalNotes;

    @SerializedName("last_modified")
    private String modifiedDate;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLabels() {
        return labels;
    }

    // TODO temp work-around for list of labels, return as one comma-separated string
    // public String getLabelsAsString() {
    // StringBuilder sb = new StringBuilder();
    // int i = 0;
    // if (labels != null && !labels.isEmpty()) {
    // int numLabelsMinusOne = labels.size() - 1;
    // for (String label : labels) {
    // sb.append(label);
    // if (i < numLabelsMinusOne) {
    // sb.append(","); // TODO make constant
    // }
    // }
    // }
    // return sb.toString();
    // }

    public void setLabels(String labels) {
        this.labels = labels;
    }

    public boolean isChecked() {
        return checked;
    }

    public void setChecked(boolean checked) {
        this.checked = checked;
    }

    public int getPosition() {
        return position;
    }

    public void setPosition(int position) {
        this.position = position;
    }

    public String getAdditionalNotes() {
        return additionalNotes;
    }

    public void setAdditionalNotes(String additionalNotes) {
        this.additionalNotes = additionalNotes;
    }

    public String getModifiedDate() {
        return modifiedDate;
    }

    public void setModifiedDate(String modifiedDate) {
        this.modifiedDate = modifiedDate;
    }

}

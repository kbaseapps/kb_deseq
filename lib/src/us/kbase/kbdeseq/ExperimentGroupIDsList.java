
package us.kbase.kbdeseq;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: ExperimentGroupIDsList</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "group_name1",
    "expr_ids1",
    "group_name2",
    "expr_ids2"
})
public class ExperimentGroupIDsList {

    @JsonProperty("group_name1")
    private java.lang.String groupName1;
    @JsonProperty("expr_ids1")
    private List<String> exprIds1;
    @JsonProperty("group_name2")
    private java.lang.String groupName2;
    @JsonProperty("expr_ids2")
    private List<String> exprIds2;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("group_name1")
    public java.lang.String getGroupName1() {
        return groupName1;
    }

    @JsonProperty("group_name1")
    public void setGroupName1(java.lang.String groupName1) {
        this.groupName1 = groupName1;
    }

    public ExperimentGroupIDsList withGroupName1(java.lang.String groupName1) {
        this.groupName1 = groupName1;
        return this;
    }

    @JsonProperty("expr_ids1")
    public List<String> getExprIds1() {
        return exprIds1;
    }

    @JsonProperty("expr_ids1")
    public void setExprIds1(List<String> exprIds1) {
        this.exprIds1 = exprIds1;
    }

    public ExperimentGroupIDsList withExprIds1(List<String> exprIds1) {
        this.exprIds1 = exprIds1;
        return this;
    }

    @JsonProperty("group_name2")
    public java.lang.String getGroupName2() {
        return groupName2;
    }

    @JsonProperty("group_name2")
    public void setGroupName2(java.lang.String groupName2) {
        this.groupName2 = groupName2;
    }

    public ExperimentGroupIDsList withGroupName2(java.lang.String groupName2) {
        this.groupName2 = groupName2;
        return this;
    }

    @JsonProperty("expr_ids2")
    public List<String> getExprIds2() {
        return exprIds2;
    }

    @JsonProperty("expr_ids2")
    public void setExprIds2(List<String> exprIds2) {
        this.exprIds2 = exprIds2;
    }

    public ExperimentGroupIDsList withExprIds2(List<String> exprIds2) {
        this.exprIds2 = exprIds2;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((("ExperimentGroupIDsList"+" [groupName1=")+ groupName1)+", exprIds1=")+ exprIds1)+", groupName2=")+ groupName2)+", exprIds2=")+ exprIds2)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

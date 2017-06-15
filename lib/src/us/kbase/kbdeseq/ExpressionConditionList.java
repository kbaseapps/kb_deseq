
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
 * <p>Original spec-file type: ExpressionConditionList</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "condition_name",
    "expression_refs"
})
public class ExpressionConditionList {

    @JsonProperty("condition_name")
    private java.lang.String conditionName;
    @JsonProperty("expression_refs")
    private List<String> expressionRefs;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("condition_name")
    public java.lang.String getConditionName() {
        return conditionName;
    }

    @JsonProperty("condition_name")
    public void setConditionName(java.lang.String conditionName) {
        this.conditionName = conditionName;
    }

    public ExpressionConditionList withConditionName(java.lang.String conditionName) {
        this.conditionName = conditionName;
        return this;
    }

    @JsonProperty("expression_refs")
    public List<String> getExpressionRefs() {
        return expressionRefs;
    }

    @JsonProperty("expression_refs")
    public void setExpressionRefs(List<String> expressionRefs) {
        this.expressionRefs = expressionRefs;
    }

    public ExpressionConditionList withExpressionRefs(List<String> expressionRefs) {
        this.expressionRefs = expressionRefs;
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
        return ((((((("ExpressionConditionList"+" [conditionName=")+ conditionName)+", expressionRefs=")+ expressionRefs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

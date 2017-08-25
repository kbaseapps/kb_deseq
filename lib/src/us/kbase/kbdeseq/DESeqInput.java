
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
 * <p>Original spec-file type: DESeqInput</p>
 * <pre>
 * required params:
 * expressionset_ref: ExpressionSet object reference
 * differential_expression_set_suffix: DifferentialExpressoinMatrixSet object suffix
 * workspace_name: the name of the workspace it gets saved to
 * optional params:
 * run_all_combinations: run all paired condition combinations
 * condition_labels: conditions for expression set object
 * alpha_cutoff: q value cutoff
 * fold_change_cutoff: fold change cutoff
 * num_threads: number of threads
 * fold_scale_type: one of ["linear", "log2+1", "log10+1"]
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "expressionset_ref",
    "differential_expression_set_suffix",
    "workspace_name",
    "run_all_combinations",
    "condition_labels",
    "alpha_cutoff",
    "fold_change_cutoff",
    "num_threads",
    "fold_scale_type"
})
public class DESeqInput {

    @JsonProperty("expressionset_ref")
    private java.lang.String expressionsetRef;
    @JsonProperty("differential_expression_set_suffix")
    private java.lang.String differentialExpressionSetSuffix;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("run_all_combinations")
    private Long runAllCombinations;
    @JsonProperty("condition_labels")
    private List<String> conditionLabels;
    @JsonProperty("alpha_cutoff")
    private Double alphaCutoff;
    @JsonProperty("fold_change_cutoff")
    private Double foldChangeCutoff;
    @JsonProperty("num_threads")
    private Long numThreads;
    @JsonProperty("fold_scale_type")
    private java.lang.String foldScaleType;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("expressionset_ref")
    public java.lang.String getExpressionsetRef() {
        return expressionsetRef;
    }

    @JsonProperty("expressionset_ref")
    public void setExpressionsetRef(java.lang.String expressionsetRef) {
        this.expressionsetRef = expressionsetRef;
    }

    public DESeqInput withExpressionsetRef(java.lang.String expressionsetRef) {
        this.expressionsetRef = expressionsetRef;
        return this;
    }

    @JsonProperty("differential_expression_set_suffix")
    public java.lang.String getDifferentialExpressionSetSuffix() {
        return differentialExpressionSetSuffix;
    }

    @JsonProperty("differential_expression_set_suffix")
    public void setDifferentialExpressionSetSuffix(java.lang.String differentialExpressionSetSuffix) {
        this.differentialExpressionSetSuffix = differentialExpressionSetSuffix;
    }

    public DESeqInput withDifferentialExpressionSetSuffix(java.lang.String differentialExpressionSetSuffix) {
        this.differentialExpressionSetSuffix = differentialExpressionSetSuffix;
        return this;
    }

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public DESeqInput withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("run_all_combinations")
    public Long getRunAllCombinations() {
        return runAllCombinations;
    }

    @JsonProperty("run_all_combinations")
    public void setRunAllCombinations(Long runAllCombinations) {
        this.runAllCombinations = runAllCombinations;
    }

    public DESeqInput withRunAllCombinations(Long runAllCombinations) {
        this.runAllCombinations = runAllCombinations;
        return this;
    }

    @JsonProperty("condition_labels")
    public List<String> getConditionLabels() {
        return conditionLabels;
    }

    @JsonProperty("condition_labels")
    public void setConditionLabels(List<String> conditionLabels) {
        this.conditionLabels = conditionLabels;
    }

    public DESeqInput withConditionLabels(List<String> conditionLabels) {
        this.conditionLabels = conditionLabels;
        return this;
    }

    @JsonProperty("alpha_cutoff")
    public Double getAlphaCutoff() {
        return alphaCutoff;
    }

    @JsonProperty("alpha_cutoff")
    public void setAlphaCutoff(Double alphaCutoff) {
        this.alphaCutoff = alphaCutoff;
    }

    public DESeqInput withAlphaCutoff(Double alphaCutoff) {
        this.alphaCutoff = alphaCutoff;
        return this;
    }

    @JsonProperty("fold_change_cutoff")
    public Double getFoldChangeCutoff() {
        return foldChangeCutoff;
    }

    @JsonProperty("fold_change_cutoff")
    public void setFoldChangeCutoff(Double foldChangeCutoff) {
        this.foldChangeCutoff = foldChangeCutoff;
    }

    public DESeqInput withFoldChangeCutoff(Double foldChangeCutoff) {
        this.foldChangeCutoff = foldChangeCutoff;
        return this;
    }

    @JsonProperty("num_threads")
    public Long getNumThreads() {
        return numThreads;
    }

    @JsonProperty("num_threads")
    public void setNumThreads(Long numThreads) {
        this.numThreads = numThreads;
    }

    public DESeqInput withNumThreads(Long numThreads) {
        this.numThreads = numThreads;
        return this;
    }

    @JsonProperty("fold_scale_type")
    public java.lang.String getFoldScaleType() {
        return foldScaleType;
    }

    @JsonProperty("fold_scale_type")
    public void setFoldScaleType(java.lang.String foldScaleType) {
        this.foldScaleType = foldScaleType;
    }

    public DESeqInput withFoldScaleType(java.lang.String foldScaleType) {
        this.foldScaleType = foldScaleType;
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
        return ((((((((((((((((((((("DESeqInput"+" [expressionsetRef=")+ expressionsetRef)+", differentialExpressionSetSuffix=")+ differentialExpressionSetSuffix)+", workspaceName=")+ workspaceName)+", runAllCombinations=")+ runAllCombinations)+", conditionLabels=")+ conditionLabels)+", alphaCutoff=")+ alphaCutoff)+", foldChangeCutoff=")+ foldChangeCutoff)+", numThreads=")+ numThreads)+", foldScaleType=")+ foldScaleType)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

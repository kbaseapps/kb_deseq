
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
 * diff_expression_obj_name: RNASeqDifferetialExpression object name
 * filtered_expression_matrix_name: name of output object filtered expression matrix
 * expr_condition_list: conditions for expression set object
 * alpha_cutoff: q value cutoff
 * num_threads: number of threads
 * workspace_name: the name of the workspace it gets saved to
 * optional params:
 * fold_scale_type: one of ["linear", "log2+1", "log10+1"]
 * fold_change_cutoff: fold change cutoff
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "expressionset_ref",
    "diff_expression_obj_name",
    "filtered_expression_matrix_name",
    "expr_condition_list",
    "alpha_cutoff",
    "num_threads",
    "workspace_name",
    "fold_scale_type",
    "fold_change_cutoff"
})
public class DESeqInput {

    @JsonProperty("expressionset_ref")
    private String expressionsetRef;
    @JsonProperty("diff_expression_obj_name")
    private String diffExpressionObjName;
    @JsonProperty("filtered_expression_matrix_name")
    private String filteredExpressionMatrixName;
    @JsonProperty("expr_condition_list")
    private List<ExpressionConditionList> exprConditionList;
    @JsonProperty("alpha_cutoff")
    private Double alphaCutoff;
    @JsonProperty("num_threads")
    private Long numThreads;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("fold_scale_type")
    private String foldScaleType;
    @JsonProperty("fold_change_cutoff")
    private Double foldChangeCutoff;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("expressionset_ref")
    public String getExpressionsetRef() {
        return expressionsetRef;
    }

    @JsonProperty("expressionset_ref")
    public void setExpressionsetRef(String expressionsetRef) {
        this.expressionsetRef = expressionsetRef;
    }

    public DESeqInput withExpressionsetRef(String expressionsetRef) {
        this.expressionsetRef = expressionsetRef;
        return this;
    }

    @JsonProperty("diff_expression_obj_name")
    public String getDiffExpressionObjName() {
        return diffExpressionObjName;
    }

    @JsonProperty("diff_expression_obj_name")
    public void setDiffExpressionObjName(String diffExpressionObjName) {
        this.diffExpressionObjName = diffExpressionObjName;
    }

    public DESeqInput withDiffExpressionObjName(String diffExpressionObjName) {
        this.diffExpressionObjName = diffExpressionObjName;
        return this;
    }

    @JsonProperty("filtered_expression_matrix_name")
    public String getFilteredExpressionMatrixName() {
        return filteredExpressionMatrixName;
    }

    @JsonProperty("filtered_expression_matrix_name")
    public void setFilteredExpressionMatrixName(String filteredExpressionMatrixName) {
        this.filteredExpressionMatrixName = filteredExpressionMatrixName;
    }

    public DESeqInput withFilteredExpressionMatrixName(String filteredExpressionMatrixName) {
        this.filteredExpressionMatrixName = filteredExpressionMatrixName;
        return this;
    }

    @JsonProperty("expr_condition_list")
    public List<ExpressionConditionList> getExprConditionList() {
        return exprConditionList;
    }

    @JsonProperty("expr_condition_list")
    public void setExprConditionList(List<ExpressionConditionList> exprConditionList) {
        this.exprConditionList = exprConditionList;
    }

    public DESeqInput withExprConditionList(List<ExpressionConditionList> exprConditionList) {
        this.exprConditionList = exprConditionList;
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

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public DESeqInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("fold_scale_type")
    public String getFoldScaleType() {
        return foldScaleType;
    }

    @JsonProperty("fold_scale_type")
    public void setFoldScaleType(String foldScaleType) {
        this.foldScaleType = foldScaleType;
    }

    public DESeqInput withFoldScaleType(String foldScaleType) {
        this.foldScaleType = foldScaleType;
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

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((("DESeqInput"+" [expressionsetRef=")+ expressionsetRef)+", diffExpressionObjName=")+ diffExpressionObjName)+", filteredExpressionMatrixName=")+ filteredExpressionMatrixName)+", exprConditionList=")+ exprConditionList)+", alphaCutoff=")+ alphaCutoff)+", numThreads=")+ numThreads)+", workspaceName=")+ workspaceName)+", foldScaleType=")+ foldScaleType)+", foldChangeCutoff=")+ foldChangeCutoff)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

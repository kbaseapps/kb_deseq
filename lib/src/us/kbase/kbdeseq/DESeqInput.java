
package us.kbase.kbdeseq;

import java.util.HashMap;
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
 * expression_set_name: ExpressionSet object name and output file header
 * filtered_expr_matrix: name of output object filtered expression matrix
 * workspace_name: the name of the workspace it gets saved to
 * fold_scale_type: one of ["linear", "log2+1", "log10+1"]
 * alpha_cutoff: q value cutoff
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "expressionset_ref",
    "diff_expression_obj_name",
    "filtered_expr_matrix",
    "workspace_name",
    "num_threads",
    "expr_ids_list",
    "fold_scale_type",
    "alpha_cutoff",
    "fold_change_cutoff",
    "maximum_num_genes"
})
public class DESeqInput {

    @JsonProperty("expressionset_ref")
    private String expressionsetRef;
    @JsonProperty("diff_expression_obj_name")
    private String diffExpressionObjName;
    @JsonProperty("filtered_expr_matrix")
    private String filteredExprMatrix;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("num_threads")
    private Long numThreads;
    /**
     * <p>Original spec-file type: ExperimentGroupIDsList</p>
     * 
     * 
     */
    @JsonProperty("expr_ids_list")
    private ExperimentGroupIDsList exprIdsList;
    @JsonProperty("fold_scale_type")
    private String foldScaleType;
    @JsonProperty("alpha_cutoff")
    private Double alphaCutoff;
    @JsonProperty("fold_change_cutoff")
    private Double foldChangeCutoff;
    @JsonProperty("maximum_num_genes")
    private Long maximumNumGenes;
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

    @JsonProperty("filtered_expr_matrix")
    public String getFilteredExprMatrix() {
        return filteredExprMatrix;
    }

    @JsonProperty("filtered_expr_matrix")
    public void setFilteredExprMatrix(String filteredExprMatrix) {
        this.filteredExprMatrix = filteredExprMatrix;
    }

    public DESeqInput withFilteredExprMatrix(String filteredExprMatrix) {
        this.filteredExprMatrix = filteredExprMatrix;
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

    /**
     * <p>Original spec-file type: ExperimentGroupIDsList</p>
     * 
     * 
     */
    @JsonProperty("expr_ids_list")
    public ExperimentGroupIDsList getExprIdsList() {
        return exprIdsList;
    }

    /**
     * <p>Original spec-file type: ExperimentGroupIDsList</p>
     * 
     * 
     */
    @JsonProperty("expr_ids_list")
    public void setExprIdsList(ExperimentGroupIDsList exprIdsList) {
        this.exprIdsList = exprIdsList;
    }

    public DESeqInput withExprIdsList(ExperimentGroupIDsList exprIdsList) {
        this.exprIdsList = exprIdsList;
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

    @JsonProperty("maximum_num_genes")
    public Long getMaximumNumGenes() {
        return maximumNumGenes;
    }

    @JsonProperty("maximum_num_genes")
    public void setMaximumNumGenes(Long maximumNumGenes) {
        this.maximumNumGenes = maximumNumGenes;
    }

    public DESeqInput withMaximumNumGenes(Long maximumNumGenes) {
        this.maximumNumGenes = maximumNumGenes;
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
        return ((((((((((((((((((((((("DESeqInput"+" [expressionsetRef=")+ expressionsetRef)+", diffExpressionObjName=")+ diffExpressionObjName)+", filteredExprMatrix=")+ filteredExprMatrix)+", workspaceName=")+ workspaceName)+", numThreads=")+ numThreads)+", exprIdsList=")+ exprIdsList)+", foldScaleType=")+ foldScaleType)+", alphaCutoff=")+ alphaCutoff)+", foldChangeCutoff=")+ foldChangeCutoff)+", maximumNumGenes=")+ maximumNumGenes)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

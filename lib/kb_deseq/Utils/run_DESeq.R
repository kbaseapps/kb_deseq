dmesg <- function( msg, ... )
  {cat("##################", msg, ..., "##################\n")}

dmesg("Running run_DESeq.R")
library(getopt, lib.loc="/kb/deployment/bin/prepDE")
library(DESeq2)
dmesg("Package Info")
sessionInfo()

option_tab = matrix(c(
                       'result_directory',   'o', 1, 'character',  #result directory
                       'condition_string',   'c', 1, 'character',  #conditions separated with comma
                       'contrast_pairs',     'p', 1, 'character',  #pairs of conditions separated with comma
                       'transcripts',        't', 0, 'logical',    #process the transcript file
                       'help',               'h', 0, 'logical'
                      ), 
                    byrow=TRUE, ncol=4);

opt = getopt(option_tab)

if (!is.null(opt$help)){
    dmesg(getopt(option_tab, usage=TRUE));
    q( status = 1 );
}

# set up input params
if (is.null(opt$transcripts)){
    input_file <- paste(opt$result_directory, "/gene_count_matrix.csv", sep='')
} else {
    input_file <- paste(opt$result_directory, "/transcript_count_matrix.csv", sep='')
}
condition_string <- opt$condition_string
contrast_pairs <- strsplit(opt$contrast_pairs, ",")[[1]]

dmesg("Start processing count matrix input")
cntTable <- read.csv(input_file, header = TRUE)
if (is.null(opt$transcripts)){
    rownames(cntTable) <- cntTable$gene_id
} else {
    rownames(cntTable) <- cntTable$transcript_id
}
cntTable <- cntTable[,-1]

conds <- factor(strsplit(condition_string, ",")[[1]])

ddsFromMatrix <- DESeqDataSetFromMatrix(cntTable, DataFrame(conds), ~ conds)
colData(ddsFromMatrix)$conds<-factor(colData(ddsFromMatrix)$conds, levels=unique(strsplit(condition_string, ",")[[1]]))
dds<-DESeq(ddsFromMatrix)
for (pair in contrast_pairs){
    gene_results_file <- paste(opt$result_directory, "/", pair, "_deseq_results.csv", sep='')
    split_pair <- strsplit(pair, "_vs_")[[1]]
    res<-results(dds, alpha=0.99999, contrast=c("conds",split_pair[2],split_pair[1]))
    res<-res[order(res$padj),]

    dmesg("DESeq2 results")
    write.csv(res, gene_results_file, row.names=TRUE)
    print(summary(res))

    # p-values for genes
    pvaluesPlot_file <- paste(opt$result_directory, "/", pair, "_pvaluesPlot.png", sep='')
    png(pvaluesPlot_file)
    hist(res$pvalue, main=paste(pair, ' transcript pvalues'), col="grey", xlab='Range of p-values')
    dev.off()

    # q-values for genes
    qvaluesPlot_file <- paste(opt$result_directory, "/", pair, "_qvaluesPlot.png", sep='')
    png(qvaluesPlot_file)
    hist(res$padj, main=paste(pair, ' transcript qvalues'), col="grey", xlab='Range of q-values')
    dev.off()

}
rld<- rlogTransformation(dds, blind=TRUE)

dmesg("Start plotting results")

# dispersion plots
deseq2_MAplot_file <- paste(opt$result_directory, "/deseq2_dispersion_plot.png", sep='')
png(deseq2_MAplot_file)
plotMA(dds, ylim=c(-2,2), main='DESeq2')
dev.off()

# PCA plots
PCA_MAplot_file <- paste(opt$result_directory, "/deseq2_PCA_plot.png", sep='')
png(PCA_MAplot_file)
plotPCA(rld, intgroup=c('conds'))
dev.off()

dmesg("Exiting run_DESeq.R")
q(save="no") 

library(getopt, lib.loc="/kb/deployment/bin/prepDE")
library(DESeq2)

dmesg <- function( msg, ... ) 
  {cat("##################", msg, ..., "##################\n")}

dmesg("Running run_DESeq.R")


option_tab = matrix(c(
                       'result_directory',   'o', 1, 'character',  #result directory
                       'condition_string',   'c', 1, 'character',  #conditions separated with comma
                       'transcripts',   't', 0, 'logical',    #process the transcript file
                       'help',               'h', 0, 'logical'
                      ), 
                    byrow=TRUE, ncol=4);

opt = getopt(option_tab)

if (!is.null(opt$help)){
    dmesg(getopt(option_tab, usage=TRUE));
    q( status = 1 );
}

dmesg("Here is the option_tab matrix of arguments")
print(option_tab)

# set up input params
if (is.null(opt$transcripts)){
    input_file <- paste(opt$result_directory, "/gene_count_matrix.csv", sep='')
} else {
    input_file <- paste(opt$result_directory, "/transcript_count_matrix.csv", sep='')
}
condition_string <- opt$condition_string
gene_results_file <- paste(opt$result_directory, "/deseq_results.csv", sep='')
# pvaluesPlot_file <- paste(opt$result_directory, "/pvaluesPlot.png", sep='')
# qvaluesPlot_file <- paste(opt$result_directory, "/qvaluesPlot.png", sep='')
deseq2_MAplot_file <- paste(opt$result_directory, "/deseq2_MAplot.png", sep='')
PCA_MAplot_file <- paste(opt$result_directory, "/PCA_MAplot.png", sep='')

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
res<-results(dds, alpha=1)
res<-res[order(res$padj),]

dmesg("DESeq2 result file head")
head(res)
write.csv(res, gene_results_file, row.names=TRUE)
summary(res)
rld<- rlogTransformation(dds, blind=TRUE)

dmesg("Start plotting results")
# p-values for genes
# png(pvaluesPlot_file)
# hist(res$pvalue, main='DESeq2 gene pvalues', col="grey", xlab='Range of p-values for genes')
# dev.off()

# q-values for genes
# png(qvaluesPlot_file)
# hist(sig_g$padj, main='DESeq2 gene qvalues', col="grey", xlab='Range of q-values for genes')
# dev.off()

# dispersion plots
png(deseq2_MAplot_file)
plotMA(dds,ylim=c(-2,2),main=paste(unique(conds)[1], 'over', unique(conds)[2]))
dev.off()

# PCA plots
png(PCA_MAplot_file)
plotPCA(rld, intgroup=c('conds'))
dev.off()

dmesg("Exiting run_DESeq.R")
q(save="no") 
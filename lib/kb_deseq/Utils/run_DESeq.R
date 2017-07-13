
library(getopt, lib.loc="/kb/deployment/bin/prepDE")
library('DESeq2')

dmesg <- function( msg, ... ) 
  {cat("##################", msg, ..., "##################\n")}

dmesg("Running run_DESeq.R")


option_tab = matrix(c(
                       'result_directory',   'o', 1, 'character',  #result directory
                       'alpha_cutoff',       'a', 1, 'double',     #alpha_cutoff
                       'fold_change_cutoff', 'f', 1, 'double',     #fold_change_cutoff
                       'condition_string',   'c', 1, 'character',  #conditions separated with comma 
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
input_file <- paste(opt$result_directory, "/gene_count_matrix.csv", sep='')
condition_string <- opt$condition_string
alpha_cutoff <- opt$alpha_cutoff
fold_change_cutoff <- opt$fold_change_cutoff
gene_results_file <- paste(opt$result_directory, "/gene_results.csv", sep='')
diff_genes_file <- paste(opt$result_directory, "/diff_genes.csv", sep='')
sig_genes_results_file <- paste(opt$result_directory, "/sig_genes_results.csv", sep='')
sig_genes_up_regulated_file <- paste(opt$result_directory, "/sig_genes_up_regulated.txt", sep='')
sig_genes_down_regulated_file <- paste(opt$result_directory, "/sig_genes_down_regulated.txt", sep='')
pvaluesPlot_file <- paste(opt$result_directory, "/pvaluesPlot.png", sep='')
qvaluesPlot_file <- paste(opt$result_directory, "/qvaluesPlot.png", sep='')
deseq2_MAplot_file <- paste(opt$result_directory, "/deseq2_MAplot.png", sep='')
PCA_MAplot_file <- paste(opt$result_directory, "/PCA_MAplot.png", sep='')

dmesg("Start processing count matrix input")
cntTable <- read.csv(input_file, header = TRUE)
rownames(cntTable) <- cntTable$gene_id
cntTable <- cntTable[,-1]

conds <- factor(strsplit(condition_string, ",")[[1]])

ddsFromMatrix <- DESeqDataSetFromMatrix(cntTable, DataFrame(conds), ~ conds)
colData(ddsFromMatrix)$conds<-factor(colData(ddsFromMatrix)$conds, levels=unique(strsplit(condition_string, ",")[[1]]))
dds<-DESeq(ddsFromMatrix)
res<-results(dds, alpha=alpha_cutoff)
res<-res[order(res$padj),]

dmesg("DESeq2 result file head")
head(res)
write.csv(res, gene_results_file, row.names=TRUE)
summary(res)
sum(res$padj < alpha_cutoff, na.rm=TRUE)
rld<- rlogTransformation(dds, blind=TRUE)
vsd<-varianceStabilizingTransformation(dds, blind=TRUE)

#  Identify genes with a q value <0.05, classify up and down regulated
sig_g=subset(res,res$padj < alpha_cutoff)
summary(sig_g)
sig_g_res <- rownames(sig_g)
write.csv(sig_g_res, diff_genes_file, row.names=FALSE)
write.csv(sig_g, sig_genes_results_file, row.names=TRUE)

sig_g_fc_up=subset(sig_g,sig_g$log2FoldChange  > fold_change_cutoff)
sig_g_fc_res_up <- rownames(sig_g_fc_up)
write.table(sig_g_fc_res_up, sig_genes_up_regulated_file, row.names=FALSE)

sig_g_fc_down=subset(sig_g,sig_g$log2FoldChange < -fold_change_cutoff)
sig_g_fc_res_down <- rownames(sig_g_fc_down)
write.table(sig_g_fc_res_down, sig_genes_down_regulated_file, row.names=FALSE)

dmesg("Start plotting results")
# p-values for genes
png(pvaluesPlot_file)
hist(res$pvalue, main='DESeq2 gene pvalues', col="grey", xlab='Range of p-values for genes')
dev.off()

# q-values for genes
png(qvaluesPlot_file)
hist(sig_g$padj, main='DESeq2 gene qvalues', col="grey", xlab='Range of q-values for genes')
dev.off()

# dispersion plots
png(deseq2_MAplot_file)
plotMA(dds,ylim=c(-2,2),main='DESeq2')
dev.off()

# PCA plots
png(PCA_MAplot_file)
plotPCA(rld, intgroup=c('conds'))
dev.off()

dmesg("Exiting run_DESeq.R")
q(save="no") 
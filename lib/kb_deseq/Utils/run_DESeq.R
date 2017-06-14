
library(getopt, lib.loc="/kb/deployment/bin/prepDE")
library('DESeq2')

dmesg <- function( msg, ... ) 
  {cat("##################", msg, ..., "##################\n")}

dmesg("Running run_DESeq.R")


option_tab = matrix(c(
                       'result_directory', 'O', 1, 'character',  #result directory
                       'output_csvfile',   'o', 1, 'character',  #output csv file
                       'help',             'h', 0, 'logical'
                      ), 
                    byrow=TRUE, ncol=4);

opt = getopt(option_tab)

if (!is.null(opt$help)){
    dmesg(getopt(option_tab, usage=TRUE));
    q( status = 1 );
}

dmesg("Here is the option_tab matrix of arguments")
print(option_tab)

print(opt$result_directory)
print(opt$output_csvfile)

dmesg("Exiting run_DESeq.R")
q(save="no") 
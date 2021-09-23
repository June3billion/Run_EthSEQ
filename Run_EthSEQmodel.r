#! /usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
#.libPaths("/home/june/R/x86_64-pc-linux-gnu-library/3.6/")
library(EthSEQ)
library(data.table)

file_input_vcf <- args[1]
file_system_model <- args[2]
dir_output <- args[3]


ethseq.Analysis(
	target.vcf = file_input_vcf,
	out.dir = dir_output,
	model.gds = file_system_model,
	cores = 8,
	space = "3D")




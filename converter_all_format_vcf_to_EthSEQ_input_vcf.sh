#!/bin/bash
date

if [ $# -ne 3 ];then
  echo "#usage: sh $0 [Tool: PLINK2] [Input File: VCF] [Output dir] "
  exit
fi

tool_plink2=$1
input_file_vcf=$2
output_dir=$3

# Reformat_VCF
${tool_plink2} \
--vcf ${input_file_vcf} \
--ref-allele force ${input_file_vcf} 4 3 \'#\' \
--set-all-var-ids @_#_\$r_\$a \
--snps-only just-acgt \
--max-alleles 2 \
--no-fid \
--recode vcf \
--out ${output_dir}/temp_vcf
date

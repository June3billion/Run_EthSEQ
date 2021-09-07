#!/bin/bash
date

if [ $# -ne 3 ];then
  echo "#usage: sh $0 [Tool: PLINK2] [Input File: VCF] [Output dir] "
  exit
fi

tool_plink2=$1
input_file_vcf=$2
output_dir=$3

# Convert VCF to PLINK
${tool_plink2} \
--vcf ${input_file_vcf} \
--ref-allele force ${input_file_vcf} 4 3 \'#\' \
--set-all-var-ids @_#_\$r_\$a \
--snps-only just-acgt \
--max-alleles 2 \
--no-fid \
--make-bed \
--out ${output_dir}/temp
date


# Convert VCF to VCF for EthSEQ
${tool_plink2} \
--bfile ${output_dir}/temp \
--recode vcf \
--out ${output_dir}/temp
date


# Run world wide EthSEQ
#${tool_Rscript} ${script_EthSEQ} \
#${output_dir}/temp.vcf \
#${file_EthSEQmodel} \
#${output_dir}/World 
#date

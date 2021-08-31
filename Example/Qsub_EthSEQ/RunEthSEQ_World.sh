date

/NAS/data/personal/june_dev/Tools/PLINK/plink  \
--vcf /NAS/data/etc/EthSEQ/Example/test_IDT.vcf \
--ref-allele force /NAS/data/etc/EthSEQ/Example/test_IDT.vcf 4 3 \'#\' \
--set-all-var-ids @_#_\$r_\$a \
--make-bed \
--out /NAS/data/etc/EthSEQ/Example//temp 

date

/NAS/data/personal/june_dev/Tools/PLINK/plink  \
--bfile /NAS/data/etc/EthSEQ/Example//temp \
--make-vcf \
--out /NAS/data/etc/EthSEQ/Example//temp 

date

/usr/bin/env Rscript  /NAS/data/etc/EthSEQ/Run_EthSEQmodel.r  \
/NAS/data/etc/EthSEQ/Example/test_IDT.vcf \
/NAS/data/etc/EthSEQ//Resource/Model_EthSEQ_IDT_World.gds \
/NAS/data/etc/EthSEQ/Example//World 
date


#!/NAS/data/etc/anaconda3/bin/python3
  
# README ####
## Authour: June (Youngjune Bhak)
## Contact: youngjune29bhak@gmail.com
## Date: 2021.08.30
## Description
### This is an ethnic group identifier. 
### It adapted EthSEQ repackage. 
### Reference models here were built based on 1KGP, resrticted by the IDT panel target region.
### This is version 1


# Preparation ####
# |---| Load libraries ####
import sys
import os
import yaml
from inspect import currentframe


# |---| Def ####
def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

# |---|  Check input, tell usage, and assgin ####
# |---|---| Check input and tell ueage ####
if len(sys.argv) < 2 :
    print("\n\n Usage: {} <Input file: /fulpath/.vcf>  <Ouput Dir: Full path for outputn dir>\n\n".format(sys.argv[0]))
    sys.exit()
# |---|---| Assign parameters ####
else:
# |---|---|---| Assign input ####
    file_input_vcf = sys.argv[1]
# |---|---|---| Assign output ####
    dir_output_report = sys.argv[2]
    if not os.path.exists(dir_output_report):
        os.makedirs(dir_output_report)
    dir_qsub = ("{}/Qsub_EthSEQ/".format(dir_output_report))
    if not os.path.exists(dir_qsub):
        os.makedirs(dir_qsub)
# |---|---|---| Assign requirements ####
    dir_system_kit= os.path.dirname(os.path.abspath(sys.argv[0]))
    try:
        config = "{}/config_EthSEQ_v1.yaml".format(dir_system_kit)
        with open(config, "r") as handle:
            config = yaml.load(handle, Loader=yaml.FullLoader)
    except IndexError:
        print("\n\nERROR: [IndexError]\nCheck paths of script and config file: {} \n Error line number: ".format(config), get_linenumber(),"\n\n")
        sys.exit()
    except FileNotFoundError:
        print("\n\nERROR: [FileNotFoundError]\nCheck paths of script and config file: {}\nError line number: ".format(config),get_linenumber(), "\n\n")
        sys.exit()

tool_plink = config["TOOL_PLINK"]
tool_Rscript = config["TOOL_RSCRIPT"]
script_Execute_EthSEQ = "{}/{}".format(dir_system_kit,config["SCRIPT_Execute_EthSEQ"])
file_system_model_IDT_world = "{}/{}".format(dir_system_kit,config["FILE_system_model_IDT_World"])
dict_SuperPopp_to_model = {"World": file_system_model_IDT_world}
file_system_model_IDT_AFR = "{}/{}".format(dir_system_kit,config["FILE_system_model_IDT_AFR"])
dict_SuperPopp_to_model["AFR"] = file_system_model_IDT_AFR
file_system_model_IDT_EUR = "{}/{}".format(dir_system_kit,config["FILE_system_model_IDT_EUR"])
dict_SuperPopp_to_model["EUR"] = file_system_model_IDT_EUR
file_system_model_IDT_AMR = "{}/{}".format(dir_system_kit,config["FILE_system_model_IDT_AMR"])
dict_SuperPopp_to_model["AMR"] = file_system_model_IDT_AMR
file_system_model_IDT_SAS = "{}/{}".format(dir_system_kit,config["FILE_system_model_IDT_SAS"])
dict_SuperPopp_to_model["SAS"] = file_system_model_IDT_SAS
file_system_model_IDT_EAS = "{}/{}".format(dir_system_kit,config["FILE_system_model_IDT_EAS"])
dict_SuperPopp_to_model["EAS"] = file_system_model_IDT_EAS




# Main 1/. Convert input VCF to EthSEQ-friendly VCF by PLINK ####
# |---| Prepare qsub ####
file_qsub = open("{}/RunEthSEQ_World.sh".format(dir_qsub),"w")
filenamepath_qsub = "{}/RunEthSEQ_World.sh".format(dir_qsub)
# |---| Convert VCF to PLINK ####
print("date", file=file_qsub, end = "\n\n")
print("{} \\".format(tool_plink), file=file_qsub)
print("--vcf {} \\".format(file_input_vcf), file=file_qsub)
print("--ref-allele force {} 4 3 \\'#\\' \\".format(file_input_vcf), file=file_qsub)
print("--set-all-var-ids @_#_\$r_\$a \\", file=file_qsub)
print("--make-bed \\", file=file_qsub)
print("--out {}/temp ".format(dir_output_report), file=file_qsub, end = "\n\n")
print("date", file=file_qsub, end = "\n\n")
# |---| Re-convert PLINK to simple VCF ####
print("{} \\".format(tool_plink), file=file_qsub)
print("--bfile {}/temp \\".format(dir_output_report), file=file_qsub)
print("--make-vcf \\", file=file_qsub)
print("--out {}/temp ".format(dir_output_report), file=file_qsub, end = "\n\n")
print("date", file=file_qsub, end = "\n\n")
# Main 2/. Get ethnic group estimation, worldwide ####
print("{} {} \\".format(tool_Rscript,script_Execute_EthSEQ),file=file_qsub)
print("{} \\".format(file_input_vcf), file=file_qsub)
print("{} \\".format(file_system_model_IDT_world), file=file_qsub)
print("{}/World ".format(dir_output_report), file=file_qsub)
print("date", file=file_qsub, end = "\n\n")
file_qsub.close()
# |---| Run and get result ####
os.system("sh {}".format(filenamepath_qsub))
os.system("cp {}/World/Report.pdf {}/PCA_World.pdf ".format(dir_output_report,dir_output_report))
name_SuperPop = (os.popen("cut -f 2 {}/World/Report.txt | tail -n 1".format(dir_output_report)).read()).replace('\n', '')
info_SuperPop = (os.popen("cut -f 2 {}/World/Report.txt | tail -n 1".format(dir_output_report)).read()).replace('\n', '')
info_SuperPop_type = (os.popen("cut -f 3 {}/World/Report.txt | tail -n 1".format(dir_output_report)).read()).replace('\n', '')
info_SuperPop_contribution = (os.popen("cut -f 4 {}/World/Report.txt | tail -n 1".format(dir_output_report)).read()).replace('\n', '')
# Main 3/. Get ethnic group estimation, population group wide, inferred from Main 2
# |---| Prepare qsub ####
file_qsub = open("{}/RunEthSEQ_Ethnic.sh".format(dir_qsub),"w")
filenamepath_qsub = "{}/RunEthSEQ_Ethnic.sh".format(dir_qsub)
print("date", file=file_qsub, end = "\n\n")
print("{} {} \\".format(tool_Rscript,script_Execute_EthSEQ),file=file_qsub)
print("{} \\".format(file_input_vcf), file=file_qsub)
print("{} \\".format(dict_SuperPopp_to_model[name_SuperPop]), file=file_qsub)
print("{}/Ethnic/ ".format(dir_output_report), file=file_qsub)
print("date", file=file_qsub, end = "\n\n")
file_qsub.close()
# |---| Run and get result ####
os.system("sh {}".format(filenamepath_qsub))
os.system("cp {}/Ethnic/Report.pdf {}/PCA_Ethinc_{}.pdf ".format(dir_output_report,dir_output_report, name_SuperPop))
info_DetailPop = (os.popen("cut -f 2 {}/Ethnic/Report.txt | tail -n 1".format(dir_output_report)).read()).replace('\n', '')
info_DetailPop_type = (os.popen("cut -f 3 {}/Ethnic/Report.txt | tail -n 1".format(dir_output_report)).read()).replace('\n', '')
info_DetailPop_contribution = (os.popen("cut -f 4 {}/Ethnic/Report.txt | tail -n 1".format(dir_output_report)).read()).replace('\n', '')
# Main 4/. Write final output
file_report = open("{}/report_ethnicity.txt".format(dir_output_report),"w")
print("SampleID\tSuperPopName\tSuperPopType\tSuperPopContribution\tDetailPopName\tDetailPopType\tDetailPopContribution",file=file_report)
print("NA\t{}\t{}\t{}\t{}\t{}\t{}".format(info_SuperPop,info_SuperPop_type,info_SuperPop_contribution,info_DetailPop,info_DetailPop_type,info_DetailPop_contribution),file=file_report)
file_report.close()




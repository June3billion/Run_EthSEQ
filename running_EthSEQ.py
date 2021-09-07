"""VCF를 받아서 인종 확인"""
"""::인종확인을 위해 EthSEQ R package를 사용"""
"""::EthSEQ 사용을 위해 input VCF을 가공"""
"""::VCF가공은 FORMAT을 GT만 남기는 것이며, PLINK2 프로그램을 이용"""
import sys
import os
import yaml
import logging
import argparse


def get_args():
    """Argparse module."""
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="### EthSEQ running with vcf")
    parser.add_argument(
        "--config", "-c", help="input config file", type=str, required=True
    )
    parser.add_argument(
        "--input", "-i", help="input vcf file", type=str, required=True
    )
    parser.add_argument(
        "--outdir", "-o", help="output directory", type=str, required=True
    )
    return parser.parse_args()


def parse_config(input_config: str):
    """[summary] config parsing module
    
    Args:
        config_file (str): config 파일
    """
    with open(input_config, "r") as handle:
        config = yaml.load(handle, Loader=yaml.FullLoader)
    return config


def reformat_vcf_for_EthSEQ(input_vcf: str, outdir: str, config: dict):
    """[summary] input VCF 받아서, PLINK2를 이용하여, EthSEQ를 위한 포맷의 VCF를 생성함 (<outdir>/temp.vcf)

    Args:
        input_vcf (str): 최초에 받은 VCF 파일
        outdir (str): 결과 파일을 저장할 경로
        config (dict): config 파일
    """
    tool = f'{os.path.dirname(os.path.realpath(__file__))}/{config["SCRIPT_reformat_VCF"]} '
    plink2 = f'{config["TOOL_PLINK2"]} '

    command = f"sh {tool} {plink2} {input_vcf} {outdir}"
    os.system(command)


def run_EthSEQ(input_vcf: str, outdir: str, config: dict, ethnicgroup=str("World")):
    """[summary] input VCF와 주어진 인종 그룹에 따라서 EthSEQ를 수행함. 기본 인종 그룹은 World

    Args:
        input_vcf (str): EthSEQ 분석을 수행할 VCF 파일 (FORMAT컬럼에 GT만 있음). 
            "reformat_vcf_for_EthSEQ" fuction을 통해 생성 가능
        outdir (str): 결과 파일을 저장할 경로
        config (dict): config 파일
        ethnicgroup (str): EthSEQ 분석을 수행할 때 이용할 인종 모델. 
            기본은 World이며 AFR (아프리카), AMR (아메리카), EUR (유럽), EAS (동부아시아), SAS (서부아시아) 선택 가능
    """
    tool = f'{config["TOOL_RSCRIPT"]} '
    tool += f'{os.path.dirname(os.path.realpath(__file__))}/{config["SCRIPT_Execute_EthSEQ"]} '
    EthSEQ_model_name_key = f"FILE_system_model_IDT_{ethnicgroup}"
    EthSEQ_model = f"{os.path.dirname(os.path.realpath(__file__))}/{config[EthSEQ_model_name_key]} "
    outdir_EthSEQ = f"{outdir}/{ethnicgroup}/"

    command = f"{tool} {input_vcf} {EthSEQ_model} {outdir_EthSEQ}"
    os.system(command)

    with open(f"{outdir_EthSEQ}/Report.txt") as handle:
        for line in handle:
            if line.startswith("sample.id"):
                header = line.strip().split("\t")
                sample_idx = header.index("sample.id")
                pop_idx = header.index("pop")
                type_idx = header.index("type")
                contribution_idx = header.index("contribution")
            data = line.strip().split("\t")
    return dict(
        sample=data[sample_idx],
        EthSEQ_result_ModelEthnicGroup = ethnicgroup,
        EthSEQ_result_ethnicgroup_classification=data[pop_idx],
        EthSEQ_result_ethnicgroup_classificaiton_type=data[type_idx],
        EthSEQ_result_ethnicgroup_classificaiton_contribution=data[contribution_idx],
    )


def write_final_EthSEQ_report(outdir: str, EthSEQ_result_ethnicwide: dict, config: dict):
    """[summary] input VCF와 주어진 인종 그룹에 따라서 EthSEQ를 수행함. 기본 인종 그룹은 World

    Args:
        outdir (str): 결과 파일을 저장할 경로
        EthSEQ_result_ethnicwide (dict): "run_EthSEQ" function의 결과. 
            (분석시 사용한 인종 그룹이 AFR (아프리카), AMR (아메리카), EUR (유럽), EAS (동부아시아), SAS (서부아시아) 중 하나 인 것)
        config (dict): config 파일

    """
    Sample = EthSEQ_result_ethnicwide["sample"]
    SuperPop_fullname = config[EthSEQ_result_ethnicwide["EthSEQ_result_ModelEthnicGroup"]]
    DetailPop_fullname = config[EthSEQ_result_ethnicwide["EthSEQ_result_ethnicgroup_classification"]]

    file_report = open(f"{outdir}/report_ethnicity.txt", "w")
    print("Sample\tSuperPop\tDetailPop",file=file_report)
    print(f"{Sample}\t{SuperPop_fullname}\t{DetailPop_fullname}",file=file_report)
    file_report.close()


def main():
    args = get_args()
    config = parse_config(args.config)
    reformat_vcf_for_EthSEQ(args.input, args.outdir, config)
    EthSEQ_result_worldwide = run_EthSEQ(f'{args.outdir}/temp.vcf',args.outdir, config)
    EthSEQ_result_ethnicwide = run_EthSEQ(f'{args.outdir}/temp.vcf',args.outdir, config, EthSEQ_result_worldwide["EthSEQ_result_ethnicgroup_classification"])
    write_final_EthSEQ_report(args.outdir,EthSEQ_result_ethnicwide,config)


if __name__ == "__main__":
    main()

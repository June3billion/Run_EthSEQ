#   README
#   Description:
#       This script identifies the sample's ethnicity based on the input sample's VCF file.
#           EthSEQ package was used for ethnicity identification.
#           This script converts the input VCF file to the EthSEQ-compatible VCF file.
#           PLINK2 was used to convert the input VCF file, by leaving only GT information of Information column.
#   Required: (Prepared with config file)
#       PLINK2 (The version used for develop: v2.00a3LM )
#       Rscript with EthSEQ installed (The versions used for develop: R = 4.1.1, EthSEQ = 2.1.4)
#   Author: June (Youngjune Bhak)
#   Contact: youngjune29bhak@gmail.com
#   Date (ver): 2021.09.24
import sys
import os
import yaml
import logging
import argparse
import subprocess
import traceback
from timeit import default_timer as timer
from datetime import timedelta


def parse_arg() -> argparse.Namespace:
    """Guide and check arguments required for this script.

    Note:
        Author: June
        Date (version): 2021.09.23

    Returns:
        argparse.Namespace: config, input, outdir

    Examples:
        >>> No arguments are required. 
            Just Use this in main function as following "args = parse_arg()" 
    """
    parser = argparse.ArgumentParser(description="#", epilog="#")
    parser.add_argument(
        "--config", "-c", help="input config file", type=str, required=True
    )
    parser.add_argument(
        "--input", "-i", help="input vcf file", type=str, required=True
    )
    parser.add_argument(
        "--outdir", "-o", help="output directory", type=str, required=True
    )
    parser.print_help()

    if not os.path.isfile(parser.parse_args().config):
        print("Function: parse_arg: Error: Invalid --config")
        sys.exit()
    if not os.access(parser.parse_args().config, os.R_OK):
        print("Function: parse_arg: Error: No permission to read --config")
        sys.exit()

    if not os.path.isfile(parser.parse_args().input):
        print("Function: parse_arg: Error: Invalid --input")
        sys.exit()
    if not os.access(parser.parse_args().input, os.R_OK):
        print("Function: parse_arg: Error: No permission to read --input")
        sys.exit()

    if not os.path.isdir(parser.parse_args().outdir):
        print("Function: parse_arg: Error: Invalid --outdir")
        sys.exit()
    if not os.access(parser.parse_args().input, os.W_OK):
        print("Function: parse_arg: Error: No permission to write --outdir")
        sys.exit()
    return parser.parse_args()


def reformat_vcf_for_EthSEQ(input_vcf: str, outdir: str, config: dict) -> None:
    """Reformat the input VCF file to the EthSEQ-compatible VCF file
        It generate EthSEQ-compatble VCF file to {outdir}/temp.vcf

    Note:
        Required: 
            PLINK2 (The version used for develop: v2.00a3LM )
        Author: June (youngjune29bhak@gmail.com)
        Date (version): 2021.09.23
        Output:
            The output file will be generates as following path and name {outdir}/temp.vcf
            
    Args:
        input_vcf (str): Input vcf file with full path
        outdir (str): output directory. 
        config (dict): config dictionary
    """
    time_start = timer()
    plink2 = config["TOOL"]["PLINK2"]
    if not os.access(plink2, os.X_OK):
        print(
            f"Function: reformat_vcf_for_EthSEQ: Error: No permission to excecute {plink2}"
        )
        sys.exit()

    reformat_cmd = plink2
    reformat_cmd += f" --vcf {input_vcf} "
    reformat_cmd += " --snps-only just-acgt --max-alleles 2 --threads 1 "
    reformat_cmd += f" --recode vcf --out {outdir}/temp "
    try:
        print("\nFunction: reformat_vcf_for_EthSEQ: Start")
        print(f"Function: reformat_vcf_for_EthSEQ: Input: {input_vcf}")
        print(
            f"Function: reformat_vcf_for_EthSEQ: Output expected: {outdir}/temp.vcf"
        )
        subprocess.run(reformat_cmd, shell=True, check=True, timeout=600)
    except subprocess.TimeoutExpired:
        print("Function: reformat_vcf_for_EthSEQ: Error: Timeout")
        sys.exit()
    except subprocess.CalledProcessError:
        print("Function: reformat_vcf_for_EthSEQ: Error: File not found")
        sys.exit()
    except subprocess.SubprocessError:
        print("Function: reformat_vcf_for_EthSEQ: Error: Subprocess Failed")
        sys.exit()

    if os.path.isfile(f"{outdir}/temp.vcf"):
        print(
            f"Function: reformat_vcf_for_EthSEQ: Output generated: {outdir}/temp.vcf"
        )
    else:
        print(
            "Function: reformat_vcf_for_EthSEQ: Finish: Faied: No output generated"
        )
        sys.exit()

    time_elapsed = timedelta(seconds=timer() - time_start)
    print(
        f"Function: reformat_vcf_for_EthSEQ: Finish: Time elapsed: '{time_elapsed}'\n"
    )


def execute_EthSEQ(
    input_vcf: str, outdir: str, config: dict, ethnicgroup=str("World")
) -> str:
    """It executes Rscript that run EthSEQ R packages with the EthSEQ-compatible VCF file
        The EthSEQ-compatible VCF file can be generated by 
        1) using "reformat_vcf_for_EthSEQ" function, or
        2) parsing the input VCF file in other ways (leave only GT from INFO column).

    Note:
        Required:
            Rscript with EthSEQ installed (designated in the config file)
            (The versions used for develop: R = 4.1.1, EthSEQ = 2.1.4)
        Author: June (youngjune29bhak@gmail.com)
        Date (version): 2021.09.23
        Args:
            ethnicgroup: Using only the Group "World" is suggested in the current version (2021.09.23),
            due to the resolution problem (can be updated once WGS is used)
        Output:
            The output file will be generates as following path and name {outdir}/Ethnicity_{ethnicgroup}-wide/Report.txt
            Also, this function returns the output file's full path as string

    Args:
        input_vcf (str): input VCF file
        outdir (str): output directory
        config (dict): config dictionary
        ethnicgroup (str): Population group to use in EthSEQ. The default is "World". 
            Addtional options are belows.
                AFR: African
                AMR: American
                EUR: European
                EAS: East Asian
                SAS: South Asian
    
    Returns:
        str: Output file path

    Examples:
        >>> execute_EthSEQ("Input VCF file", "Outdir", "Config dictionary")
        >>> execute_EthSEQ("input.vcf", "./", {'key': 'value'}, "World") 
        >>> -> ./World/Report.txt
    """
    time_start = timer()
    Rscript = config["TOOL"]["RSCRIPT"]
    script_EthSEQ = f'{os.path.dirname(os.path.realpath(__file__))}/{config["SCRIPT"]["R_Execute_EthSEQ"]}'
    if not os.access(Rscript, os.X_OK):
        print(
            f"Function: reformat_vcf_for_EthSEQ: Error: No permission to excecute: {Rscript}"
        )
        sys.exit()
    if not os.access(script_EthSEQ, os.X_OK,):
        print(
            f"Function: reformat_vcf_for_EthSEQ: Error: No permission to excecute: {script_EthSEQ}"
        )
        sys.exit()

    tool = f"{Rscript} {script_EthSEQ}"
    EthSEQ_model_path = f"{os.path.dirname(os.path.realpath(__file__))}"
    EthSEQ_model_name = f'{config["GDS"][ethnicgroup]}'
    EthSEQ_model = f"{EthSEQ_model_path}/{EthSEQ_model_name}"
    outdir_EthSEQ = f"{outdir}/Ethnicity_{ethnicgroup}-wide"

    EthSEQ_cmd = f"{tool} {input_vcf} {EthSEQ_model} {outdir_EthSEQ}"
    try:
        print("\nFunction: run_EthSEQ: Start")
        print(f"Function: run_EthSEQ: Input: {outdir}/temp.vcf")
        print(
            f"Function: run_EthSEQ: Output expected: {outdir_EthSEQ}/Report.txt"
        )
        subprocess.run(EthSEQ_cmd, shell=True, check=True)
    except subprocess.TimeoutExpired:
        print("Function: run_EthSEQ: Error: Timeout")
        sys.exit()
    except subprocess.CalledProcessError:
        print("Function: run_EthSEQ: Error: File not found")
        sys.exit()
    except subprocess.SubprocessError:
        print("Function: run_EthSEQ: Error: Subprocess Failed")
        sys.exit()

    if os.path.isfile(f"{outdir_EthSEQ}/Report.txt"):
        print(
            f"Function: run_EthSEQ: Output generated: {outdir_EthSEQ}/Report.txt"
        )
    else:
        print("Function: run_EthSEQ: Finish: Faied: No output generated")
        sys.exit()

    time_elapsed = timedelta(seconds=timer() - time_start)
    print(f"Function: run_EthSEQ: Finish: Time elapsed: '{time_elapsed}'\n")
    return f"{outdir_EthSEQ}/Report.txt"


def main():
    args = parse_arg()
    time_start = timer()
    print("running_EthSEQ.py: Start\n")

    config = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    reformat_vcf_for_EthSEQ(args.input, args.outdir, config)
    EthSEQ_report = execute_EthSEQ(
        f"{args.outdir}/temp.vcf", args.outdir, config
    )
    print(f"\nrunning_EthSEQ.py: Output generated: {EthSEQ_report}")

    # Place for the GEBRA submission
    # Place for the GEBRA submission
    # Place for the GEBRA submission

    time_elapsed = timedelta(seconds=timer() - time_start)
    print(f"running_EthSEQ.py: Finish: Time elapsed: '{time_elapsed}'\n")


if __name__ == "__main__":
    main()

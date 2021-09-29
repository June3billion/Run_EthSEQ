import sys
import os
import yaml
import argparse
import subprocess
from timeit import default_timer as timer
from datetime import timedelta
from running_EthSEQ import *
import pytest


def test_reformat_vcf_for_EthSEQ():
    """Reformat the input VCF file to the EthSEQ-compatible VCF file
        It generate EthSEQ-compatble VCF file to {outdir}/temp.vcf

    Note:
        Required:
            PLINK2 (The version used for develop: v2.00a3LM )
        Author: June (youngjune29bhak@gmail.com)
        Date (version): 2021.09.29
        Output:
            The output file will be generates as following path and name {outdir}/temp.vcf

    Args:
        input_vcf (str): Input vcf file with full path
        outdir (str): output directory.
        config (dict): config dictionary
    """

    input_vcf = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/Example/EPA21-EAOG.final.vcf.gz"
    outdir = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/Example/"
    file_config = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/config_EthSEQ.yaml"
    config = yaml.load(open(file_config, "r"), Loader=yaml.FullLoader)

    reformat_vcf_for_EthSEQ(input_vcf, outdir, config)

    output_expected = f"{outdir}/temp.vcf"
    assert os.path.isfile(output_expected)


def test_execute_EthSEQ() -> str:
    """It executes Rscript that run EthSEQ R packages with the EthSEQ-compatible VCF file
        The EthSEQ-compatible VCF file can be generated by
        1) using "reformat_vcf_for_EthSEQ" function, or
        2) parsing the input VCF file in other ways (leave only GT from INFO column).

    Note:
        Required:
            Rscript with EthSEQ installed (designated in the config file)
            (The versions used for develop: R = 4.1.1, EthSEQ = 2.1.4)
        Author: June (youngjune29bhak@gmail.com)
        Date (version): 2021.09.29
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
    outdir = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/Example/"
    input_vcf = (
        "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/Example/temp.vcf"
    )
    file_config = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/config_EthSEQ.yaml"
    config = yaml.load(open(file_config, "r"), Loader=yaml.FullLoader)
    ethnicgroup = "World"
    output_generated_from_execute_EthSEQ = execute_EthSEQ(
        input_vcf, outdir, config, ethnicgroup
    )
    assert os.path.isfile(output_generated_from_execute_EthSEQ)

from running_EthSEQ import *

def test_parse_config():
    """config file을 parsing 하는 기능"""
    input_config = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/config_EthSEQ.yaml"
    config = parse_config(input_config)
    assert config["EUR"] == "European"


def test_run_EthSEQ():
    """ 인종판별프로그램인 EthSEQ가 주어진 VCF 를 가지고 인종을 판별 하는 지 확인"""
    input_vcf = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/Example/Test_new_R/temp.vcf"
    outdir = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/Example/Test_new_R/"
    input_config = "/NAS/data/personal/june_dev/Git/Run_EthSEQ/Run_EthSEQ/config_EthSEQ.yaml"
    config =  parse_config(input_config)
    ethnicgroup = "World"
    result_EthSEQ = run_EthSEQ(input_vcf, outdir, config, ethnicgroup)
    assert result_EthSEQ["EthSEQ_result_ethnicgroup_classification"] == "EUR"

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import subprocess
import argparse


def connect_to_drive(credential_file):
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scope)
    gc = gspread.authorize(credentials)
    return gc

def collect_gdrive_data(credential_file):
    gc = connect_to_drive(credential_file)
    sheet_obj = gc.open("Meta data sheet for drought comparison project").sheet1
    Data = sheet_obj.get_all_values()
    Headers = Data.pop(1)
    Data.pop(0)
    df = pd.DataFrame(Data, columns=Headers)
    return df


def write_srr(outdir, df, species):
    with open(os.path.join(outdir,"sample_file_list.txt"), "w+") as outfile:
        for srr in df.loc[df["Species"] == species]["SRA_number"]:
            outfile.write(srr+"\n")
    n_samples = len(df.loc[df["Species"] == species]["SRA_number"])
    return n_samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outdir", help="directory where samples will be downloaded")
    parser.add_argument("-c", "--credential", help="path to google drive credential JSON file", default="/mnt/research/VanBuren_Lab/01_code/05_credentials/gdrive_credentials.json")
    parser.add_argument("-s", "--species", help="binomial name of species to download data for")
    parser.add_argument("sd", "--script_dir", help="path to the directory containing this script", default="./")
    args = parser.parse_args()
    outdir = args.outdir
    credential_file = args.credential
    species = args.species
    script_dir = args.script_dir
    df = collect_gdrive_data(credential_file)
    n_samples = write_srr(outdir, df, species)
    shell_script = os.path.join(script_dir, "slurm_batch_sra_download.sh")
    subprocess.call(["sbatch",
                     "--array=0-"+str(n_samples),
                     shell_script,
                     outdir])


if __name__ == "__main__":
    main()

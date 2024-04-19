import subprocess
import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Run FastQC on sequencing data and generate quality reports.")
    parser.add_argument("-i", "--inputs", nargs='+', required=True, help="Paths to input FASTQ files or directories containing FASTQ files")
    parser.add_argument("-o", "--output_dir", required=True, help="Directory to store the FastQC reports")
    return parser.parse_args()

def run_fastqc(inputs, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a list of files if directories are provided
    fastq_files = []
    for input_path in inputs:
        if os.path.isdir(input_path):
            for file in os.listdir(input_path):
                if file.endswith('.fastq') or file.endswith('.fq'):
                    fastq_files.append(os.path.join(input_path, file))
        else:
            fastq_files.append(input_path)
    
    # Run FastQC on each file
    for file in fastq_files:
        command = ['fastqc', file, '--outdir', output_dir]
        try:
            subprocess.run(command, check=True)
            print(f"FastQC completed for {file}")
        except subprocess.CalledProcessError as e:
            print(f"FastQC failed for {file}: {e}", file=sys.stderr)

def main():
    args = parse_args()
    run_fastqc(args.inputs, args.output_dir)

if __name__ == "__main__":
    main()

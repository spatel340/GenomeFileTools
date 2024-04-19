import subprocess
import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Align sequencing reads to a reference genome.")
    parser.add_argument("-r", "--reference", required=True, help="Path to the reference genome")
    parser.add_argument("-i", "--input", required=True, help="Path to the input FASTQ or BAM file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output SAM/BAM file")
    parser.add_argument("--aligner", choices=['bwa', 'bowtie'], default='bwa', help="Alignment tool to use (default: bwa)")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads to use (default: 4)")
    return parser.parse_args()

def check_tool_installed(tool_name):
    """Check if the specified tool is installed."""
    from shutil import which
    return which(tool_name) is not None

def run_alignment(args):
    if args.aligner == 'bwa':
        command = [
            'bwa', 'mem',
            '-t', str(args.threads),
            args.reference,
            args.input,
            '>',
            args.output
        ]
    elif args.aligner == 'bowtie':
        command = [
            'bowtie',
            '-p', str(args.threads),
            '-S',
            args.reference,
            args.input,
            args.output
        ]

    # Join command list into a single string for subprocess
    command = " ".join(command)
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Alignment complete: {args.output}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during alignment: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    args = parse_args()
    if not check_tool_installed(args.aligner):
        print(f"{args.aligner} is not installed. Please install it and try again.", file=sys.stderr)
        sys.exit(1)

    run_alignment(args)

if __name__ == "__main__":
    main()

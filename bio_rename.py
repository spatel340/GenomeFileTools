import os
import logging
import argparse

def setup_logging():
    logging.basicConfig(filename='rename_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rename_func(dir_name, ignored_extensions, ignored_prefixes):
    for root, dirs, files in os.walk(dir_name, topdown=False):
        for file in files:
            filename, extension = os.path.splitext(file)
            if extension in ignored_extensions or any(filename.startswith(prefix) for prefix in ignored_prefixes):
                logging.info(f'Skipped: {file}')
                continue
            new_name = f"{os.path.basename(root)}_{filename[-5:]}{extension}"
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, new_name)
            try:
                os.rename(old_path, new_path)
                logging.info(f'Renamed: {file} to {new_name}')
            except Exception as e:
                logging.error(f'Failed to rename {file}: {str(e)}')

def main():
    parser = argparse.ArgumentParser(description="Rename files in a directory based on specific rules for bioinformatics.")
    parser.add_argument('dir', type=str, help='Directory to process')
    parser.add_argument('--ignore_ext', nargs='*', default=['.py', '.sql', '.R', '.sh'], help='File extensions to ignore')
    parser.add_argument('--ignore_prefix', nargs='*', default=['barcodes', 'gdc', 'geneList'], help='Filename prefixes to ignore')
    
    args = parser.parse_args()
    
    setup_logging()
    rename_func(args.dir, set(args.ignore_ext), set(args.ignore_prefix))

if __name__ == '__main__':
    main()

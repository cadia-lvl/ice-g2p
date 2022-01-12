#
# A complete grapheme-to-phoneme module for Icelandic.
# Transcribes graphemes (alphabetic text) to phonemes with or without the help of a pronunciation dictionary.
# Output is according to input: a wordlist as input produces a dictionary formatted output word\ttranscription,
# text as input produces a line by line transcription text\ttranscription.
#
# Syllabification and stress labeling is optional.
#
# Examples:
#
#

import os
import sys
import logging
import argparse
from pathlib import Path

from . import syllab_stress_processing as syllabify
from .g2p_lstm import FairseqG2P


def write_transcribed(transcribed: dict, filename: Path, suffix: str, keep_original: bool) -> None:
    """
    Writes the transcriptions with the original grapheme strings to a file
    named 'filename' extended by 'suffix', for example:
    original filename: path/to/textfile.txt
    output filename: path/to/textfile_transcribed.tsv

    :param transcribed: a map with grapheme strings as keys and phonetic transcr. as values
    :param filename: the original filename containing the grapheme strings
    :param suffix: the suffix to label the output file with
    :param keep_original: write the original grapheme string in the first column
    :return:
    """
    filename_stem = filename.stem
    extended_filename = str(filename.parent) + '/' + filename_stem + suffix + '.tsv'
    with open(extended_filename, 'w') as f:
        for key in transcribed:
            if keep_original:
                f.write(key + '\t')
            f.write(transcribed[key] + '\n')


def extract_transcript(syllabified: list) -> str:
    result = ''
    for entr in syllabified:
        if not result:
            result += entr.simple_stress_format()
        else:
            result += '. ' + entr.simple_stress_format()

    return result

def process_string(input_str: str, syllab=False, use_dict=False, word_sep=False) -> str:
    print('processing: "' + input_str + '"')
    g2p = FairseqG2P()
    if syllab:
        transcr_arr = []
        for wrd in input_str.split(' '):
            transcr_arr.append(g2p.transcribe(wrd.strip(), use_dict, False))
        entries = syllabify.init_pron_dict_from_dict(dict(zip(input_str.split(' '), transcr_arr)))
        transcribed = extract_transcript(syllabify.syllabify_and_label(entries))
    else:
        transcribed = g2p.transcribe(input_str.strip(), use_dict, word_sep)
    return transcribed


def process_file(filename: Path, syllab=False, use_dict=True, word_sep=False) -> dict:
    """
    Transcribes the content of 'filename' line by line
    :param filename: input file to transcribe
    :param word_sep: if the transcription should contain word separators
    :return: a map of grapheme strings and their phonetic transcriptions
    """
    print("processing: " + str(filename))
    g2p = FairseqG2P()
    with open(filename) as f:
        file_content = f.read().splitlines()

    transcribed = {}
    for line in file_content:
        if syllab:
            transcr_arr = []
            for wrd in line.split(' '):
                transcr_arr.append(g2p.transcribe(wrd.strip(), use_dict, False))
            entries = syllabify.init_pron_dict_from_dict(dict(zip(line.split(' '), transcr_arr)))
            transcribed[line] = extract_transcript(syllabify.syllabify_and_label(entries))
        else:
            transcribed[line] = g2p.transcribe(line.strip(), use_dict, word_sep)

    return transcribed


def process_file_or_dir(file_or_dir: Path, out_suffix: str, syllab=False, use_dict=False, word_sep=False, keep_original=False) -> None:
    print("processing: " + str(file_or_dir))
    if os.path.isdir(file_or_dir):
        for root, dirs, files in os.walk(file_or_dir):
            for filename in files:
                if filename.startswith('.'):
                    continue
                file_path = Path(os.path.join(root, filename))
                transcribed_content = process_file(file_path, syllab, use_dict, word_sep)
                write_transcribed(transcribed_content, file_path, out_suffix, keep_original)
    elif os.path.isfile(file_or_dir):
        transcribed_content = process_file(file_or_dir, use_dict, word_sep)
        write_transcribed(transcribed_content, file_or_dir, out_suffix, keep_original)


def get_arguments():
    parser = argparse.ArgumentParser(description='Transcribe text input to phonetic representation. Provide '
                                                 'an input file or directory, or a string on stdin to transcribe.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--infile', '-if', type=Path, help='inputfile or directory')
    group.add_argument('--inputstr', '-i', help='input string')
    parser.add_argument('--keep', '-k', action='store_true', help='keep original')
    parser.add_argument('--sep', '-s', action='store_true', help='use word separator')
    parser.add_argument('--dict', '-d', action='store_true', help='use pronunciation dictionary')
    parser.add_argument('--syll', '-y', action='store_true', help='add syllabification and stree labeling')
    return parser.parse_args()


def main():
    args = get_arguments()
    keep_original = args.keep
    word_sep = args.sep
    use_dict = args.dict
    syllab = args.syll
    # we need either an input file or directory, or a string from stdin
    if args.infile is not None:
        if not args.infile.exists():
            logging.error(str(args.infile) + ' does not exist.')
            sys.exit(1)
        else:
            process_file_or_dir(args.infile, '_transcribed', syllab, use_dict, word_sep, keep_original)

    if args.inputstr is not None:
        if keep_original:
            print(args.inputstr + ' : ' + process_string(args.inputstr, syllab, use_dict, word_sep))
        else:
            print(process_string(args.inputstr, syllab, use_dict, word_sep))


if __name__ == '__main__':
    main()
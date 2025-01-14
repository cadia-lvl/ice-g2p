# Ice-g2p : Phonetic transcription (grapheme-to-phoneme) for Icelandic

Ice-g2p is a module for automatic phonetic transcription of Icelandic.

## Setup

Clone the repository and create a virtual environment in the project root directory. Install the requirements:

    git clone git@github.com:grammatek/ice-g2p.git
	cd ice-g2p
	python -m venv g2p-venv
	source g2p-venv/bin/activate
	pip install -r requirements.txt



## Command line interface

**The input strings/texts need to be normalized. The module only handles lowercase characters from the Icelandic alphabet, no punctuation or other characters, unless language detection is enabled (see Flags)**

Characters allowed: _[aábcðdeéfghiíjklmnoóprstuúvxyýzþæö]_. If other characters are found in the input, the transcription of the respective token is skipped and a notice written to stdout.

To transcribe text, currently two main options are available, direct from stdin to stdout or from file or a collection of files (directory) 

    %python src/ice-g2p/main.py -i 'hljóðrita þetta takk'
	l_0 j ou D r I t a T E h t a t_h a h k

	%python src/ice-g2p/main.py -if file_to_transcribe.txt

If the input comes from stdin, the output is written to stdout. Input from file(s) is written to file(s) with the same name with the suffix '_transcribed.tsv'. The files are transcribed line by line and written out correspondingly. 

### Flags

The options available:

    --infile INFILE, -if INFILE
                        inputfile or directory
  	--inputstr INPUTSTR, -i INPUTSTR
                          input string
  	--keep, -k            keep original
  	--sep, -s             use word separator
	--dict, -d            use pronunciation dictionary
	--syll, -y            add syllabification and stress labeling
	--langdetect, -l      use word-based language detection

Using the `-k` flag keeps the original grapheme strings and for file input/output writes the original strings in the first column of the tab separated output file, and the phonetic transcription in the second one.
The `-s`flag adds a word separator to the transcription. With the `-d` flag all tokens are first looked up in an existing pronunciation dictionary, the automatic g2p is then only a fallback for words not contained in the dictionary. With the `-y` flag syllabification and stress labeling is added to the transcription:

    %python src/ice-g2p/main.py -i 'hljóðrita þetta takk' -k -s
	hljóðrita þetta takk : l_0 j ou D r I t a-T E h t a-t_h a h k

	%python src/ice-g2p/main.py -i 'hljóðrita þetta takk' -k -y
	hljóðrita þetta takk : l_0 j ou1 D. r I0. t a0. T E1 h. t a0. t_h a1 h k

Using the `-l` flag allows for word-based language detection, where words considered foreign are transcribed by an LSTM trained on English words instead of Icelandic. If this flag is used, the module can handle common non-Icelandic characters, including all of the English alphabet:

    %python src/ice-g2p/main.py -i 'hljóðrita þetta please'
	l_0 j ou D r I t a T E h t a t_h a p_h l E: a s E
	
	%python src/ice-g2p/main.py -i 'hljóðrita þetta please' -l
	l_0 j ou D r I t a T E h t a p_h l i: s

## Trouble shooting & inquiries

This application is still in development. If you encounter any errors, feel free to open an issue inside the
[issue tracker](https://github.com/grammatek/ice-g2p/issues). You can also [contact us](mailto:info@grammatek.com) via email.

## Contributing

You can contribute to this project by forking it, creating a private branch and opening a new [pull request](https://github.com/grammatek/ice-g2p/pulls).  

## License

[![Grammatek](grammatek-logo-small.png)](https://www.grammatek.com)

Copyright © 2020, 2021 Grammatek ehf.

This software is developed under the auspices of the Icelandic Government 5-Year Language Technology Program, described
[here](https://www.stjornarradid.is/lisalib/getfile.aspx?itemid=56f6368e-54f0-11e7-941a-005056bc530c) and
[here](https://clarin.is/media/uploads/mlt-en.pdf) (English).

This software is licensed under the [Apache License](LICENSE)

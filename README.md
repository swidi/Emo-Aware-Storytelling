# PO-EMO generation

This repository contains the code for the experiment we did in our term paper 'Modeling and Generation of Emotion and Emotion Arcsin Prose and Poetry'. It is largely based on the code of 
[Modeling Protagonist Emotions for Emotion-Aware Storytelling](https://www.aclweb.org/anthology/2020.emnlp-main.426/)                                                                                              *Faeze Brahman, and Snigdha Chaturvedi.* EMNLP 2020 and uses the [PO-EMO dataset](https://arxiv.org/abs/2003.07723).

**Data files includes**:
1. `[train/test/dev]_x1.txt`: titles
2. `[train/test/dev]_x4.txt`: stanzas
3. `[train/test/dev]_mapped.txt`: stanza emotions

## Code

* The code depends on a patched version of [Texar](https://github.com/asyml/texar). Please install the version under [third_party/texar](./third_party/texar). Follow the installation instructions in the README there.
* Download gpt-2-M from [here](https://github.com/openai/gpt-2) and put it in `gpt2_pretrained_models/` folder.
* Use `prepare_poemo.py` to process PO-EMO's tsv format
* Use `translate.py` to translate the german dataset into english
* Use `cat` to concatenate the english and german dataset
* Use `split.py` for the train/test/dev split
* Use `prepare_data.py` to preprocess the data and transform them into TFRecord format. An example command is (please see the code for more config options).
```bash
python prepare_data.py --data_dir=data

```
* Run `run_emosup.sh` for training/testing the model. (please see config files for more config options.)

### Interactive Generation
First, download the pretrained model from [here](https://drive.google.com/file/d/1l6kbXg644ANJ9MxyH_V8pl5TrxzuPgBJ/view?usp=sharing) and untar it:
```
tar -xvzf model.tar.gz
```
Then run following command to interactively generate emotion-aware stories:
```bash
sh run_interactive.sh
```
Running that, it will ask you to first enter a Title, and then a sequence of emotions separated by space. For example: joy sadness sadness

The code is adapted from [Counterfactual Story Generation](https://github.com/qkaren/Counterfactual-StoryRW).

## Reference

This experiment is largely based on this work:
```
@inproceedings{brahman-chaturvedi-2020-modeling,
    title = "Modeling Protagonist Emotions for Emotion-Aware Storytelling",
    author = "Brahman, Faeze  and
      Chaturvedi, Snigdha",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.426",
    pages = "5277--5294"
}
```

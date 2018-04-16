# MultiRC: Reasoning over Mulitple Sentences [![Build Status](https://semaphoreci.com/api/v1/projects/bcb461fa-0d0f-4580-ad3b-4d39afa861c9/1308311/badge.svg)](https://semaphoreci.com/danyaljj/hard-qa)

This repo contains the necessary code for a few baselines and evaluation reported used in the paper. To read more details on the paper, refer to [this page](http://cogcomp.org/page/publication_view/831) or [the dataset page](http://cogcomp.org/multirc/). 

## Evaluation 
The evaluation script used is included in the `eval/` folder. To test the usage, use sample input and outpu files in the folder: 
```
python3.5 
```

## Baselines 
The baselines are written in Java/Scala. The code also contains classes for reading the questions. 

## Citation 
If you use this, please cite the paper: 

```
@inproceedings{MultiRC2018,
    author = {Daniel Khashabi and Snigdha Chaturvedi and Michael Roth and Shyam Upadhyay and Dan Roth},
    title = {Looking Beyond the Surface:A Challenge Set for Reading Comprehension over Multiple Sentences},
    booktitle = {NAACL},
    year = {2018}
}
```

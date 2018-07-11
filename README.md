# MultiRC: Reasoning over Mulitple Sentences 

This repo contains a few useful in this work. To read more details on the paper, refer to [this page](http://cogcomp.org/page/publication_view/831) or [the dataset page](http://cogcomp.org/multirc/). 

## Evaluation 
The evaluation script used is included in the `eval/` folder.  

To get F1 measures: 

```bash
> python eval/multirc-eval-v1.py 
Per question measures (i.e. precision-recall per question, then average) 
        P: 0.825211112777 - R: 0.907502623295 - F1m: 0.864402738925
Dataset-wide measures (i.e. precision-recall across all the candidate-answers in the dataset) 
        P: 0.82434611161 - R: 0.906551362683 - F1a: 0.86349665639
```

To get a Precision-Recall curve: 
```bash
> python eval/multirc-pr-curve-v1.py
```
which should give you something like the following: 


![](eval/pr-curve-output.png  | width=100)


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

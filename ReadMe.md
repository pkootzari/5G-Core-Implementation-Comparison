Tested with python 3.11.5 for generating secuiry report.


To create the **security report** for comparing each image's vulnerability between Clair and Trivy, run:

```
python compareReport.py
```

It will generate an output, named "image_comparison_results.log".


To create the **security report** for comparing each prototype's vulnerability, run:

```
python comparePrototypes.py
```

It will generate an output, named "prototype_comparison_results.log".
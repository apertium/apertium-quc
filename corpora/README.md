# Corpora

## Example

This corpus consists of a small set of test sentences which illustrate the different formats and conversions.

* `example.src`: The output of the morphological analyser in Apertium format
* `example.dep`: The dependency trees in VISLCG3 format 
  * The input is `example.ref`, it is passed through `cg-conv -a -l` and then hand-annotated for dependencies
* `example.ref`: The tagged (hand-disambiguated) output of the morphological analyser
* `example.seg`: The segmented generation of the tagged output

The files `example.dep` and `example.seg` can be used to generate CoNLL-U output.

## UTexas

* `utexas.tagged`:

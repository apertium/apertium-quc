stats() {
echo "========================================================================="
sta=`hfst-summarise $1 | grep '^# of [sa]' | tr '\n' ' '`;
siz=`ls -sh $1`;
echo $siz" "$sta;
hfst-fst2strings -w -r 1 $1

}
for nsteps in 10 25 50 100 150 200 250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000; do
	mkdir models/$nsteps
	pushd models/$nsteps
	cat /home/fran/corpora/languages/kiche/*/quc.crp.txt | apertium -d ~/source/apertium/languages/apertium-quc quc-morph | sed 's/\$[^\^]\+\^/$ ^/g' | sed 's/\/[^\$]\+\$//g' | sed 's/\^/ /g' | sed 's/  */ /g' | sed 's/^ *//g' > quc.tokenised.txt
	wc -lw quc.tokenised.txt
	~/source/subword-nmt/learn_joint_bpe_and_vocab.py --symbols $nsteps --input quc.tokenised.txt --output quc.tokenised.bpe.txt --write-vocabulary quc.tokenised.vocab.txt
	cat quc.tokenised.vocab.txt | grep '@@' | python3 ../../foo.py  | hfst-strings2fst -j -o quc.nonfin.hfst
	cat quc.tokenised.vocab.txt | grep -v '@@' | python3 ../../foo.py fin  | hfst-strings2fst -j -o quc.fin.hfst
	
	hfst-repeat quc.nonfin.hfst -o quc.nonfin.cycle.hfst
	stats quc.nonfin.cycle.hfst
	hfst-concatenate -1 quc.nonfin.cycle.hfst -2 quc.fin.hfst -o quc.cycle-fin.hfst
	stats quc.cycle-fin.hfst
	hfst-union -1 quc.fin.hfst -2 quc.cycle-fin.hfst  | hfst-minimise -E -o quc.segments.hfst
	stats quc.segments.hfst
	
	hfst-compose -F -1 ../../../../quc.gen.hfst -2 quc.segments.hfst | hfst-minimise -E -o quc.gen.segments-weighted.hfst
	stats quc.gen.segments-weighted.hfst
	hfst-subtract -1 ../../../../quc.gen.hfst -2 quc.gen.segments-weighted.hfst |hfst-minimise -E -o quc.gen.unweighted.hfst
	stats quc.gen.unweighted.hfst
	hfst-reweight -e -a 1 quc.gen.unweighted.hfst -o quc.gen.uniform.hfst
	stats quc.gen.uniform.hfst
	hfst-union -1 quc.gen.segments-weighted.hfst -2 quc.gen.uniform.hfst | hfst-eliminate-flags | hfst-minimise -E -o quc.gen.weighted.hfst
	stats quc.gen.weighted.hfst
	
	hfst-compose-intersect -e -1 quc.gen.weighted.hfst -2 ../../../../quc.mor.twol.hfst -o quc.gen.weighted.phon.hfst 
	stats quc.gen.weighted.phon.hfst
	hfst-compose -F -1 quc.gen.weighted.phon.hfst -2 ../../../../quc.spellrelax.hfst | hfst-invert -o quc.mor.weighted.hfst
	stats quc.mor.weighted.hfst
	hfst-fst2fst -w quc.mor.weighted.hfst -o quc.automorf.weighted.hfst
	stats quc.automorf.weighted.hfst
	
	cat ~/corpora/languages/kiche/bible/quc.hitparade.txt | apertium-destxt | hfst-proc -w ../../../../quc.automorf.hfst  | apertium-retxt > quc.hitparade.old
	cat ~/corpora/languages/kiche/bible/quc.hitparade.txt | apertium-destxt | hfst-proc -w quc.automorf.weighted.hfst  | apertium-retxt > quc.hitparade.new
	
	cat quc.hitparade.old | grep '\*' | wc -l
	cat quc.hitparade.new | grep '\*' | wc -l

	cat ../../../../eval/utexas.ref | cut -f2 -d'^' | cut -f1 -d'/' | hfst-proc -N 1 quc.automorf.weighted.hfst  > utexas.weights

	python3 ../../../../eval/estimate-morph.py ../../../../eval/utexas.ref utexas.weights token > results.txt

	popd
done

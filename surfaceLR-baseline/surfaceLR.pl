#!/usr/bin/perl
use lib '.';

use JSON;
use strict;

# helper variables
my $origtext = "";
my $text = "";
my $question = "";
my $type = "";
my $answer = "";

# hash that maps feature names to ids
my %features = ();
# inverse hash of features
my %reversef = ();

# Length and overlap features proposed by MITRE:
# "... the following three counts were added to the feature set: |S overlap A|, ..."
foreach ("t_length_word", "t_length_char", "a_length_word", "a_length_char", "q_length_word", "q_length_char", 
	 "ta_overlap", "qa_overlap", "tq_overlap") {
    $features{$_} = 1 + scalar(keys %features);
    $reversef{$features{$_}} = $_;
}

# process each data file, but start with train 
# (features need to be defined before processing the test sets!)
foreach my $data ("train", "test_0", "test_1", "test_2", "test_3", "test_4") {
    process($data."_".($data eq "train"?456:83).".json");
}

# process method takes a filename as input 
# and selects suitable processor to create output
sub process($) {
    my $filename = shift;
    processJSON($filename) if($filename =~ m/\.json$/);
}

# processor for JSON
sub processJSON($) {
    my $filename = shift;
    my ($data) = ($filename =~ m/(.*)_[^_]*$/);

    # open file 
    open(IN, $filename) or die "Could not open file: $filename!\n";
    #if(-e "multRC_$data.preds") {
    #open(PRED, "multRC_$data.preds");
    #} else {
    open(OUT, ">multRC_$data.feats");
    #}
    
    my $json;
    while(<IN>) {
	# read each line as a JSON object and extract corresponding data
	$json = decode_json $_;
	foreach (@{$json->{"data"}}) {
	    $origtext = $_->{"paragraph"}->{"text"};
	    $origtext =~ s/<[^\/]*\/[^>]*>//g;
	    $origtext =~ s/<[^>]*>//g;

	    # read and normalize text (=lowercase, tokenize, ...)
	    $text = normalize($origtext);
	    
	    foreach (@{$_->{"paragraph"}->{"questions"}}) {

		# read and normalize each question
		$question = $_->{"question"};
		$question = normalize($question);
		
		foreach (@{$_->{"answers"}}) {

		    # read and normalize each answer
		    $answer = $_->{"text"};
		    $answer = normalize($answer);

		    # build JSON output, if predictions already available
 		    if (-e "multRC_$data.preds") {
			my $pred = <PRED>;
			chomp $pred;
			($pred) = ($pred =~ m/ ([^ ]*) /);

			$_->{"scores"}->{"simpleLR"} = $pred;
		    } else {

			my $correct = $_->{"isAnswer"};		    
			print OUT $correct?"1":"0";
			# extract features and write to file (LIBLINEAR)
			writefeats(featurize($text, $question, $answer), $data);
		    }
		}		    
	    }
	}
    }
    close(IN);

    if($data =~ m/train/) {
	`liblinear/train -c 1 -n 20 -B 1 -s 0 multRC_train.feats`;
    } else {
	`liblinear/predict -b 1 multRC_$data.feats multRC_train.feats.model multRC_$data.preds`;
	open(PRED, "multRC_$data.preds");	
	open(IN, $filename) or die "Could not open file: $filename!\n";
	my $json;
	while(<IN>) {
	    # read each line as a JSON object and extract corresponding data
	    $json = decode_json $_;
	    foreach (@{$json->{"data"}}) {
		foreach (@{$_->{"paragraph"}->{"questions"}}) {
		    foreach (@{$_->{"answers"}}) {
			my $pred = <PRED>;
			chomp $pred;
			($pred) = ($pred =~ m/ ([^ ]*) /);			
			$_->{"scores"}->{"simpleLR"} = $pred;
		    }
		}
	    }
	}		
	
	open(OUT, ">$data.withLRscores.json");
	print OUT encode_json $json;
	close(PRED);
	close(IN);
    }
    close(OUT);
}

# writefeats takes a set of features and name of dataset as 
# input and then writes out a corresponding feature file in
# the LIBLINEAR format (LABEL [FEATID:FEATVAL]*\n)
sub writefeats($$) {
    my $features = shift;
    my $data = shift;

    my @f = @$features;
    
    push @f, "t_length_char";
    push @f, "t_length_word";
    push @f, "q_length_char";
    push @f, "q_length_word";
    push @f, "a_length_char";
    push @f, "a_length_word";

    my %feats = ();    
    
    foreach (@f) {
	# if feature hasn't been seen before, assign feature ID
	# (requires current dataset to be the training data)     
	if(!$features{$_}) {
	    next unless ($data =~ m/train/);
	    $features{$_} = 1 + scalar(keys %features);
	    $reversef{$features{$_}} = $_;
	}
	
	# fill feature values for length/overlap features
	if(m/_length_/) {
	    my $str = "";
	    $str = $text if(m/^t/);
	    $str = $question if(m/^q/);
	    $str = $answer if (m/^a/);
	    if(m/_char$/) {
		$feats{$features{$_}} = length($str);
	    } elsif(m/_word$/) {
		$feats{$features{$_}} = scalar(split(" ", $str));
	    }

	# default treatment for other features (just count them)     
	} else {
	    $feats{$features{$_}}++;	
	}
    }

    # write features, ordered by ID (required by LIBLINEAR)
    my @feats = sort {$a <=> $b} keys %feats;
    foreach (@feats) {
	print OUT " ", $_, ":", $feats{$_};
    }
    print OUT "\n";
}

# normalize take a string as input (text, question or answer)
# and produces a "normalized" output
sub normalize($) {
    my $string = shift;

    # lowercase input
    $string = lc($string);

    # replace HTML quotation marks with actual quotation marks
    $string =~ s/&quot;/"/g;

    # remove punctuation and extra spaces
    $string =~ s/([\(\),\.\?\!\":\'\/])/ /g;
    $string =~ s/  */ /g;

    return $string;
}

# featurize takes a <text, question, answer> triple as input
# and extracts all applicable features from that triple
sub featurize($$$) {
    my $t = shift;
    my $q = shift;
    my $a = shift;

    # tokenize by whitespace
    my @t = split(" ", $t);
    my @q = split(" ", $q);
    my @a = split(" ", $a);

    # start with an empty list of features
    my @features = ();

    # find "prominent" words, i.e. more often than average
    my %prominent = ();
    my $total = 0;
    my $avg = 0;
    if(@t) {
	foreach (@t) {
	    $total++;
	    $prominent{$_}++;
	}
	$avg = scalar(keys %prominent)/$total;
	foreach (keys %prominent) {
	    undef $prominent{$_} unless($prominent{$_} > $avg);
	}
    }

    # this variable keeps track of already extracted features
    # => make sure that counts represent types, not tokens
    my %overlap = ();

    ##########################################################
    # All features below are modified adaptations from MITRE #
    ##########################################################
   
    # "set of words in the answer (A)"
    foreach (@a) {
	if(!$overlap{$_}) {
	    push @features, "a".$_."_type";
	    if($prominent{$_}) {
		push @features, "t".$_."xa".$_."_prominenttype";
		push @features, "ta_prominent_typeoverlap";
	    }
	}
	
	$overlap{$_}++;
    }

    # "the words common to the story and the answer ("S")"
    %overlap = ();
    foreach my $x (@t) {
	foreach my $y (@a) {
	    if($x eq $y) {
		if(!$overlap{$x}) {
		    push @features, "t".$x."xa".$y."_type";
		    push @features, "ta_overlap_type"
		}
		$overlap{$x}++;
	    }
	}
	foreach my $y (@q) {
	    push @features, "tq_overlap" if($x eq $y);
	}
    }

    # "the Cartesian product of the the(sic!) question and the answer (Q x A)"
    %overlap = ();
    foreach my $x (@q) {
	foreach my $y (@a) {
	    if(!$overlap{$x."_x_".$y}) {
		push @features, "q".$x."xa".$y."_type";
		push @features, "qa_overlap_type" if($x eq $y);
	    }
	    $overlap{$x."_x_".$y}++;
	}
    }
    
    return \@features;
}



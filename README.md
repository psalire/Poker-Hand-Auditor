
# Poker Hand Auditor (with Confidence Intervals)

This script calculates proportion of card draws and hands compared to the expected values in confidence intervals. These are the same methods as shown in iTechlabs' [example audit report](https://itechlabs.com/certification-services/rtprng-audits/), which is one of the leaders in RNG audits for casinos.

Also included is the option to do the same with hole card pairs.

iTechlabs also uses Marsaglia's "diehard" tests which are not covered in this script.

## How it works

It parses hand history files for hole and board cards while counting every drawn card, and all 5-card hands and their ranks (e.g. pair, straight, etc.). Optionally, also count the hole card distribution and/or the distribution of all hand combinations of hole and board cards. Final output is tables of the found sample proportions compared to the expected with upper and lower confidence limits.

## Prerequisites

- Python 3 (3.9.1)
- treys (`python -m pip install treys`) - [A poker hand evaluation library](https://github.com/ihendley/treys)

## Files

```
main.py  - Main script for output
Parse.py - Parsing hand history files
```

## How to use

Locate the directory where your poker client saves hand history. Run with `python main.py "C:\path\to\your\hand_history"`. See usage below for more options.

### Site Support

Parsing is only supported for Bovada hand history currently. To add parsing for other sites, create a new class in `Parse.py` with same methods as class `Bovada`.

On Bovada, you have to manually download hand history for each game in the accounts tab of the client. It then saves the hand history on Windows to `C:\Users\username\Bovada.lv Poker\Hand History\`.

### Usage

```
usage: main.py [-h] [--allcombinations] [--onlyme] [--holecards]
               [--holecardswithsuits] [--stdev {1,2,3}] [--site {Bovada}]
               path

Poker Hand Auditor

positional arguments:
  path                  Path to hand history directory

optional arguments:
  -h, --help            show this help message and exit
  --allcombinations     Show table for frequency of all combinations between
                        hole and board cards.
  --onlyme              Only count my hands
  --holecards           Show table for frequency of hole cards without suits
  --holecardswithsuits  Show table for frequency of hole cards with suits
                        (Long output)
  --stdev {1,2,3}       Stdev for confidence limit, so 1 for 68%, 2 for 95%,
                        and 3 for 99.7%. Default=2
  --site {Bovada}       Which site's hand history is being parsed.
                        Default=Bovada
```

### Sample output

```
> python main.py "C:\Users\psalire\Bovada.lv Poker\Hand History\012345678910" --stdev 3 --holecards

------------------------------------------------------------------------------------------------------------------
                              Distribution of Hands, 99.7% Confidence Limit, n=44365                              
------------------------------------------------------------------------------------------------------------------
       Hand        |   Expected    |    Sample     |     Lower     |     Upper     | Expected Size |  Sample Size
------------------------------------------------------------------------------------------------------------------
    high card      |   0.501177    |   0.285022    |   0.487838    |   0.514516    |     22235     |     12645    
       pair        |   0.422569    |   0.440099    |   0.411964    |   0.433174    |     18747     |     19525    
     two pair      |   0.047539    |   0.166663    |   0.040115    |   0.054963    |     2109      |     7394     
 three of a kind   |   0.021128    |   0.038792    |   0.010728    |   0.031528    |      937      |     1721     
     straight      |   0.003925    |   0.031331    |   -0.001106   |   0.008956    |      174      |     1390     
      flush        |   0.001965    |   0.020737    |   -0.002415   |   0.006345    |      87       |      920     
    full house     |   0.001441    |   0.015868    |   -0.002848   |   0.005730    |      64       |      704     
  four of a kind   |   0.000240    |   0.001285    |   -0.005915   |   0.006395    |      11       |      57      
  straight flush   |   0.000015    |   0.000203    |   -0.003914   |   0.003945    |       1       |       9      
------------------------------------------------------------------------------------------------------------------
      Total        |   0.999999    |   1.000000    |   0.934446    |   1.065552    |     44365     |     44365    

------------------------------------------------------------------------------------------------------------------
                     Distribution of All Hand Combinations, 99.7% Confidence Limit, n=579070                      
------------------------------------------------------------------------------------------------------------------
       Hand        |   Expected    |    Sample     |     Lower     |     Upper     | Expected Size |  Sample Size
------------------------------------------------------------------------------------------------------------------
    high card      |   0.501177    |   0.494885    |   0.498375    |   0.503979    |    290217     |    286573    
       pair        |   0.422569    |   0.426814    |   0.419588    |   0.425550    |    244697     |    247155    
     two pair      |   0.047539    |   0.048523    |   0.043731    |   0.051347    |     27528     |     28098    
 three of a kind   |   0.021128    |   0.021557    |   0.017267    |   0.024989    |     12235     |     12483    
     straight      |   0.003925    |   0.004214    |   0.000128    |   0.007722    |     2273      |     2440     
      flush        |   0.001965    |   0.002243    |   -0.001721   |   0.005651    |     1138      |     1299     
    full house     |   0.001441    |   0.001482    |   -0.002444   |   0.005326    |      834      |      858     
  four of a kind   |   0.000240    |   0.000266    |   -0.003505   |   0.003985    |      139      |      154     
  straight flush   |   0.000015    |   0.000017    |   -0.003712   |   0.003743    |       9       |      10      
------------------------------------------------------------------------------------------------------------------
      Total        |   0.999999    |   1.000000    |   0.967706    |   1.032293    |    579070     |    579070    

----------------------------------------------------------------------------------
                         Distribution of Cards, n=157174                          
----------------------------------------------------------------------------------
       Card        |   Expected    |    Sample     | Expected Size |  Sample Size
----------------------------------------------------------------------------------
        2c         |   0.019231    |   0.019399    |     3023      |     3049     
        2d         |   0.019231    |   0.018712    |     3023      |     2941     
        2h         |   0.019231    |   0.019176    |     3023      |     3014     
        2s         |   0.019231    |   0.019755    |     3023      |     3105     
        3c         |   0.019231    |   0.019323    |     3023      |     3037     
        3d         |   0.019231    |   0.018979    |     3023      |     2983     
        3h         |   0.019231    |   0.018871    |     3023      |     2966     
        3s         |   0.019231    |   0.019361    |     3023      |     3043     
        4c         |   0.019231    |   0.019310    |     3023      |     3035     
        4d         |   0.019231    |   0.019278    |     3023      |     3030     
        4h         |   0.019231    |   0.019316    |     3023      |     3036     
        4s         |   0.019231    |   0.019062    |     3023      |     2996     
        5c         |   0.019231    |   0.019653    |     3023      |     3089     
        5d         |   0.019231    |   0.019342    |     3023      |     3040     
        5h         |   0.019231    |   0.019221    |     3023      |     3021     
        5s         |   0.019231    |   0.019335    |     3023      |     3039     
        6c         |   0.019231    |   0.019577    |     3023      |     3077     
        6d         |   0.019231    |   0.019647    |     3023      |     3088     
        6h         |   0.019231    |   0.018896    |     3023      |     2970     
        6s         |   0.019231    |   0.019532    |     3023      |     3070     
        7c         |   0.019231    |   0.019348    |     3023      |     3041     
        7d         |   0.019231    |   0.018852    |     3023      |     2963     
        7h         |   0.019231    |   0.019195    |     3023      |     3017     
        7s         |   0.019231    |   0.019157    |     3023      |     3011     
        8c         |   0.019231    |   0.019144    |     3023      |     3009     
        8d         |   0.019231    |   0.019291    |     3023      |     3032     
        8h         |   0.019231    |   0.019100    |     3023      |     3002     
        8s         |   0.019231    |   0.019698    |     3023      |     3096     
        9c         |   0.019231    |   0.018985    |     3023      |     2984     
        9d         |   0.019231    |   0.019221    |     3023      |     3021     
        9h         |   0.019231    |   0.019991    |     3023      |     3142     
        9s         |   0.019231    |   0.019036    |     3023      |     2992     
        Tc         |   0.019231    |   0.019125    |     3023      |     3006     
        Td         |   0.019231    |   0.019183    |     3023      |     3015     
        Th         |   0.019231    |   0.019208    |     3023      |     3019     
        Ts         |   0.019231    |   0.019602    |     3023      |     3081     
        Jc         |   0.019231    |   0.018896    |     3023      |     2970     
        Jd         |   0.019231    |   0.019272    |     3023      |     3029     
        Jh         |   0.019231    |   0.019195    |     3023      |     3017     
        Js         |   0.019231    |   0.019259    |     3023      |     3027     
        Qc         |   0.019231    |   0.018712    |     3023      |     2941     
        Qd         |   0.019231    |   0.018699    |     3023      |     2939     
        Qh         |   0.019231    |   0.019214    |     3023      |     3020     
        Qs         |   0.019231    |   0.019660    |     3023      |     3090     
        Kc         |   0.019231    |   0.019259    |     3023      |     3027     
        Kd         |   0.019231    |   0.019393    |     3023      |     3048     
        Kh         |   0.019231    |   0.019189    |     3023      |     3016     
        Ks         |   0.019231    |   0.019361    |     3023      |     3043     
        Ac         |   0.019231    |   0.018896    |     3023      |     2970     
        Ad         |   0.019231    |   0.018922    |     3023      |     2974     
        Ah         |   0.019231    |   0.018941    |     3023      |     2977     
        As         |   0.019231    |   0.019253    |     3023      |     3026     
----------------------------------------------------------------------------------
      Total        |   1.000000    |   1.000000    |    157196     |    157174    

----------------------------------------------------------------------------------
                Distribution of Hole Cards without suits, n=65236                 
----------------------------------------------------------------------------------
    Hole Cards     |   Expected    |    Sample     | Expected Size |  Sample Size
----------------------------------------------------------------------------------
       2 2         |   0.004525    |   0.004338    |      295      |      283     
       2 3         |   0.012066    |   0.011895    |      787      |      776     
       2 4         |   0.012066    |   0.011681    |      787      |      762     
       2 5         |   0.012066    |   0.012876    |      787      |      840     
       2 6         |   0.012066    |   0.012187    |      787      |      795     
       2 7         |   0.012066    |   0.012141    |      787      |      792     
       2 8         |   0.012066    |   0.012355    |      787      |      806     
       2 9         |   0.012066    |   0.012462    |      787      |      813     
       2 T         |   0.012066    |   0.012187    |      787      |      795     
       2 J         |   0.012066    |   0.012278    |      787      |      801     
       2 Q         |   0.012066    |   0.011727    |      787      |      765     
       2 K         |   0.012066    |   0.012631    |      787      |      824     
       2 A         |   0.012066    |   0.011420    |      787      |      745     
       3 3         |   0.004525    |   0.004323    |      295      |      282     
       3 4         |   0.012066    |   0.012294    |      787      |      802     
       3 5         |   0.012066    |   0.012049    |      787      |      786     
       3 6         |   0.012066    |   0.012570    |      787      |      820     
       3 7         |   0.012066    |   0.012447    |      787      |      812     
       3 8         |   0.012066    |   0.011527    |      787      |      752     
       3 9         |   0.012066    |   0.011512    |      787      |      751     
       3 T         |   0.012066    |   0.012248    |      787      |      799     
       3 J         |   0.012066    |   0.011481    |      787      |      749     
       3 Q         |   0.012066    |   0.011895    |      787      |      776     
       3 K         |   0.012066    |   0.012049    |      787      |      786     
       3 A         |   0.012066    |   0.011773    |      787      |      768     
       4 4         |   0.004525    |   0.004875    |      295      |      318     
       4 5         |   0.012066    |   0.011926    |      787      |      778     
       4 6         |   0.012066    |   0.011435    |      787      |      746     
       4 7         |   0.012066    |   0.011803    |      787      |      770     
       4 8         |   0.012066    |   0.011665    |      787      |      761     
       4 9         |   0.012066    |   0.011543    |      787      |      753     
       4 T         |   0.012066    |   0.011696    |      787      |      763     
       4 J         |   0.012066    |   0.012386    |      787      |      808     
       4 Q         |   0.012066    |   0.012217    |      787      |      797     
       4 K         |   0.012066    |   0.012095    |      787      |      789     
       4 A         |   0.012066    |   0.012141    |      787      |      792     
       5 5         |   0.004525    |   0.004185    |      295      |      273     
       5 6         |   0.012066    |   0.011558    |      787      |      754     
       5 7         |   0.012066    |   0.011941    |      787      |      779     
       5 8         |   0.012066    |   0.012386    |      787      |      808     
       5 9         |   0.012066    |   0.012018    |      787      |      784     
       5 T         |   0.012066    |   0.012263    |      787      |      800     
       5 J         |   0.012066    |   0.012324    |      787      |      804     
       5 Q         |   0.012066    |   0.012064    |      787      |      787     
       5 K         |   0.012066    |   0.012754    |      787      |      832     
       5 A         |   0.012066    |   0.012263    |      787      |      800     
       6 6         |   0.004525    |   0.004231    |      295      |      276     
       6 7         |   0.012066    |   0.011711    |      787      |      764     
       6 8         |   0.012066    |   0.012800    |      787      |      835     
       6 9         |   0.012066    |   0.011987    |      787      |      782     
       6 T         |   0.012066    |   0.012386    |      787      |      808     
       6 J         |   0.012066    |   0.012324    |      787      |      804     
       6 Q         |   0.012066    |   0.011481    |      787      |      749     
       6 K         |   0.012066    |   0.012539    |      787      |      818     
       6 A         |   0.012066    |   0.013060    |      787      |      852     
       7 7         |   0.004525    |   0.004537    |      295      |      296     
       7 8         |   0.012066    |   0.012079    |      787      |      788     
       7 9         |   0.012066    |   0.011957    |      787      |      780     
       7 T         |   0.012066    |   0.012003    |      787      |      783     
       7 J         |   0.012066    |   0.012187    |      787      |      795     
       7 Q         |   0.012066    |   0.012401    |      787      |      809     
       7 K         |   0.012066    |   0.012095    |      787      |      789     
       7 A         |   0.012066    |   0.011466    |      787      |      748     
       8 8         |   0.004525    |   0.004384    |      295      |      286     
       8 9         |   0.012066    |   0.012324    |      787      |      804     
       8 T         |   0.012066    |   0.012416    |      787      |      810     
       8 J         |   0.012066    |   0.012018    |      787      |      784     
       8 Q         |   0.012066    |   0.012600    |      787      |      822     
       8 K         |   0.012066    |   0.011742    |      787      |      766     
       8 A         |   0.012066    |   0.012294    |      787      |      802     
       9 9         |   0.004525    |   0.004461    |      295      |      291     
       9 T         |   0.012066    |   0.011849    |      787      |      773     
       9 J         |   0.012066    |   0.012217    |      787      |      797     
       9 Q         |   0.012066    |   0.012416    |      787      |      810     
       9 K         |   0.012066    |   0.012370    |      787      |      807     
       9 A         |   0.012066    |   0.012447    |      787      |      812     
       T T         |   0.004525    |   0.004599    |      295      |      300     
       T J         |   0.012066    |   0.012018    |      787      |      784     
       T Q         |   0.012066    |   0.011267    |      787      |      735     
       T K         |   0.012066    |   0.012386    |      787      |      808     
       T A         |   0.012066    |   0.012033    |      787      |      785     
       J J         |   0.004525    |   0.003909    |      295      |      255     
       J Q         |   0.012066    |   0.012324    |      787      |      804     
       J K         |   0.012066    |   0.012003    |      787      |      783     
       J A         |   0.012066    |   0.012263    |      787      |      800     
       Q Q         |   0.004525    |   0.004476    |      295      |      292     
       Q K         |   0.012066    |   0.011987    |      787      |      782     
       Q A         |   0.012066    |   0.011727    |      787      |      765     
       K K         |   0.004525    |   0.004369    |      295      |      285     
       K A         |   0.012066    |   0.011742    |      787      |      766     
       A A         |   0.004525    |   0.004231    |      295      |      276     
----------------------------------------------------------------------------------
      Total        |   1.000000    |   1.000000    |     65221     |     65236    
```

## Interpreting Results

Above in the sample output looking at the second table showing all hand combinations, it was found that the "high card" and "pair" sample values are not within the lower and upper values of the 99.7% confidence interval. The high card sample value was below the lower, and the pair sample value was above the upper 99.7% confidence limit. This means these that sample values fall within 0.3% of the expected outcomes given the current sample size, which is extremely unusual but still not completely impossible.

However, when looking at the first table showing the actual hand distribution of the sample, it's clear that the distribution is very irregular. All hands except for four of a kind and straight fall significantly outside of the 99.7% confidence interval. In addition, the most common hand by far was a pair, not high card as is expected.

This sample shows an invalid RNG algorithm. More samples are needed to reach a conclusion.

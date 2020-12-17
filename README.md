
# Poker Hand Auditor (with Confidence Intervals)

This script calculates proportion of card draws and hands compared to the expected values in confidence intervals. These are the same methods as shown in iTechlabs' [example audit report](https://itechlabs.com/certification-services/rtprng-audits/), which is the leader in RNG audits for casinos.

Also included is the option to do the same with hole card pairs.

iTechlabs also uses Marsaglia's "diehard" tests which are not covered in this script.

## How it works

It parses hand history files for hole cards and board cards while counting every drawn card, and all combinations of 5-card hands and their ranks (e.g. pair, straight, etc.) between the hole cards and board cards. etc. Optionally, also count hole card pairs. Final output is tables of the found sample proportions with upper and lower confidence limits.

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
usage: main.py [-h] [--onlyme] [--holecards] [--holecardsnosuits]
               [--stdev {1,2,3}] [--site {Bovada}]
               path

Poker Hand Auditor

positional arguments:
  path                Path to hand history directory

optional arguments:
  -h, --help          show this help message and exit
  --onlyme            Only count my hands
  --holecards         Show table for frequency of hole cards with suits (Long
                      output)
  --holecardsnosuits  Show table for frequency of hole cards without suits
  --stdev {1,2,3}     Stdev for confidence limit, so 1 for 68%, 2 for 95%, and
                      3 for 99.7%. Default=2
  --site {Bovada}     Which site's hand history is being parsed.
                      Default=Bovada
```

### Sample output

```
> python main.py "C:\Users\psalire\Bovada.lv Poker\Hand History\012345678910" --stdev 3 --holecardsnosuits

---------------------------------------------------------------------------------------------
                   Distribution of Hands, 99.7% Confidence Limit, n=571201                   
---------------------------------------------------------------------------------------------
       Hand        |   Expected   |    Sample    |    Lower     |    Upper     |     Size    
---------------------------------------------------------------------------------------------
    high card      |   0.501177   |   0.495106   |   0.498356   |   0.503998   |    282805   
       pair        |   0.422569   |   0.426704   |   0.419567   |   0.425571   |    243734   
     two pair      |   0.047539   |   0.048526   |   0.043705   |   0.051373   |    27718    
 three of a kind   |   0.021128   |   0.021443   |   0.017230   |   0.025026   |    12248    
     straight      |   0.003925   |   0.004224   |   0.000106   |   0.007744   |     2413    
      flush        |   0.001965   |   0.002241   |  -0.001748   |   0.005678   |     1280    
    full house     |   0.001441   |   0.001478   |  -0.002476   |   0.005358   |     844     
  four of a kind   |   0.000240   |   0.000261   |  -0.003567   |   0.004047   |     149     
  straight flush   |   0.000015   |   0.000018   |  -0.003712   |   0.003743   |      10     
---------------------------------------------------------------------------------------------
       Sum         |   0.999999   |   1.000000   |   0.967461   |   1.032538   |    571201   

---------------------------------------------------------------
                Distribution of Cards, n=154740                
---------------------------------------------------------------
       Card        |   Expected   |    Sample    |     Size    
---------------------------------------------------------------
        2c         |   0.019231   |   0.019426   |     3006    
        2d         |   0.019231   |   0.018676   |     2890    
        2h         |   0.019231   |   0.019187   |     2969    
        2s         |   0.019231   |   0.019736   |     3054    
        3c         |   0.019231   |   0.019329   |     2991    
        3d         |   0.019231   |   0.018922   |     2928    
        3h         |   0.019231   |   0.018864   |     2919    
        3s         |   0.019231   |   0.019368   |     2997    
        4c         |   0.019231   |   0.019310   |     2988    
        4d         |   0.019231   |   0.019284   |     2984    
        4h         |   0.019231   |   0.019349   |     2994    
        4s         |   0.019231   |   0.019058   |     2949    
        5c         |   0.019231   |   0.019685   |     3046    
        5d         |   0.019231   |   0.019362   |     2996    
        5h         |   0.019231   |   0.019219   |     2974    
        5s         |   0.019231   |   0.019381   |     2999    
        6c         |   0.019231   |   0.019568   |     3028    
        6d         |   0.019231   |   0.019646   |     3040    
        6h         |   0.019231   |   0.018857   |     2918    
        6s         |   0.019231   |   0.019581   |     3030    
        7c         |   0.019231   |   0.019297   |     2986    
        7d         |   0.019231   |   0.018857   |     2918    
        7h         |   0.019231   |   0.019232   |     2976    
        7s         |   0.019231   |   0.019122   |     2959    
        8c         |   0.019231   |   0.019174   |     2967    
        8d         |   0.019231   |   0.019284   |     2984    
        8h         |   0.019231   |   0.019064   |     2950    
        8s         |   0.019231   |   0.019691   |     3047    
        9c         |   0.019231   |   0.018922   |     2928    
        9d         |   0.019231   |   0.019200   |     2971    
        9h         |   0.019231   |   0.020027   |     3099    
        9s         |   0.019231   |   0.019025   |     2944    
        Tc         |   0.019231   |   0.019193   |     2970    
        Td         |   0.019231   |   0.019174   |     2967    
        Th         |   0.019231   |   0.019168   |     2966    
        Ts         |   0.019231   |   0.019607   |     3034    
        Jc         |   0.019231   |   0.018896   |     2924    
        Jd         |   0.019231   |   0.019232   |     2976    
        Jh         |   0.019231   |   0.019148   |     2963    
        Js         |   0.019231   |   0.019265   |     2981    
        Qc         |   0.019231   |   0.018735   |     2899    
        Qd         |   0.019231   |   0.018689   |     2892    
        Qh         |   0.019231   |   0.019226   |     2975    
        Qs         |   0.019231   |   0.019710   |     3050    
        Kc         |   0.019231   |   0.019239   |     2977    
        Kd         |   0.019231   |   0.019471   |     3013    
        Kh         |   0.019231   |   0.019155   |     2964    
        Ks         |   0.019231   |   0.019329   |     2991    
        Ac         |   0.019231   |   0.018903   |     2925    
        Ad         |   0.019231   |   0.018948   |     2932    
        Ah         |   0.019231   |   0.018922   |     2928    
        As         |   0.019231   |   0.019284   |     2984    
---------------------------------------------------------------
       Sum         |   1.000000   |   1.000000   |    154740   

 ---------------------------------------------------------------
       Distribution of Hole Cards without suits, n=64226       
---------------------------------------------------------------
    Hole Cards     |   Expected   |    Sample    |     Size    
---------------------------------------------------------------
       2 2         |   0.004525   |   0.004266   |     274     
       2 3         |   0.012066   |   0.011895   |     764     
       2 4         |   0.012066   |   0.011740   |     754     
       2 5         |   0.012066   |   0.012845   |     825     
       2 6         |   0.012066   |   0.012191   |     783     
       2 7         |   0.012066   |   0.012176   |     782     
       2 8         |   0.012066   |   0.012316   |     791     
       2 9         |   0.012066   |   0.012487   |     802     
       2 T         |   0.012066   |   0.012207   |     784     
       2 J         |   0.012066   |   0.012269   |     788     
       2 Q         |   0.012066   |   0.011740   |     754     
       2 K         |   0.012066   |   0.012612   |     810     
       2 A         |   0.012066   |   0.011460   |     736     
       3 3         |   0.004525   |   0.004235   |     272     
       3 4         |   0.012066   |   0.012191   |     783     
       3 5         |   0.012066   |   0.012082   |     776     
       3 6         |   0.012066   |   0.012643   |     812     
       3 7         |   0.012066   |   0.012440   |     799     
       3 8         |   0.012066   |   0.011537   |     741     
       3 9         |   0.012066   |   0.011553   |     742     
       3 T         |   0.012066   |   0.012222   |     785     
       3 J         |   0.012066   |   0.011491   |     738     
       3 Q         |   0.012066   |   0.011958   |     768     
       3 K         |   0.012066   |   0.012067   |     775     
       3 A         |   0.012066   |   0.011724   |     753     
       4 4         |   0.004525   |   0.004858   |     312     
       4 5         |   0.012066   |   0.011958   |     768     
       4 6         |   0.012066   |   0.011460   |     736     
       4 7         |   0.012066   |   0.011833   |     760     
       4 8         |   0.012066   |   0.011615   |     746     
       4 9         |   0.012066   |   0.011506   |     739     
       4 T         |   0.012066   |   0.011693   |     751     
       4 J         |   0.012066   |   0.012394   |     796     
       4 Q         |   0.012066   |   0.012285   |     789     
       4 K         |   0.012066   |   0.012145   |     780     
       4 A         |   0.012066   |   0.012145   |     780     
       5 5         |   0.004525   |   0.004204   |     270     
       5 6         |   0.012066   |   0.011631   |     747     
       5 7         |   0.012066   |   0.011989   |     770     
       5 8         |   0.012066   |   0.012409   |     797     
       5 9         |   0.012066   |   0.011989   |     770     
       5 T         |   0.012066   |   0.012269   |     788     
       5 J         |   0.012066   |   0.012254   |     787     
       5 Q         |   0.012066   |   0.012160   |     781     
       5 K         |   0.012066   |   0.012736   |     818     
       5 A         |   0.012066   |   0.012191   |     783     
       6 6         |   0.004525   |   0.004235   |     272     
       6 7         |   0.012066   |   0.011631   |     747     
       6 8         |   0.012066   |   0.012690   |     815     
       6 9         |   0.012066   |   0.012004   |     771     
       6 T         |   0.012066   |   0.012425   |     798     
       6 J         |   0.012066   |   0.012300   |     790     
       6 Q         |   0.012066   |   0.011428   |     734     
       6 K         |   0.012066   |   0.012549   |     806     
       6 A         |   0.012066   |   0.013079   |     840     
       7 7         |   0.004525   |   0.004531   |     291     
       7 8         |   0.012066   |   0.012129   |     779     
       7 9         |   0.012066   |   0.011864   |     762     
       7 T         |   0.012066   |   0.012036   |     773     
       7 J         |   0.012066   |   0.012176   |     782     
       7 Q         |   0.012066   |   0.012331   |     792     
       7 K         |   0.012066   |   0.012082   |     776     
       7 A         |   0.012066   |   0.011413   |     733     
       8 8         |   0.004525   |   0.004422   |     284     
       8 9         |   0.012066   |   0.012331   |     792     
       8 T         |   0.012066   |   0.012487   |     802     
       8 J         |   0.012066   |   0.011958   |     768     
       8 Q         |   0.012066   |   0.012674   |     814     
       8 K         |   0.012066   |   0.011724   |     753     
       8 A         |   0.012066   |   0.012285   |     789     
       9 9         |   0.004525   |   0.004469   |     287     
       9 T         |   0.012066   |   0.011895   |     764     
       9 J         |   0.012066   |   0.012207   |     784     
       9 Q         |   0.012066   |   0.012409   |     797     
       9 K         |   0.012066   |   0.012347   |     793     
       9 A         |   0.012066   |   0.012456   |     800     
       T T         |   0.004525   |   0.004593   |     295     
       T J         |   0.012066   |   0.012067   |     775     
       T Q         |   0.012066   |   0.011226   |     721     
       T K         |   0.012066   |   0.012269   |     788     
       T A         |   0.012066   |   0.012020   |     772     
       J J         |   0.004525   |   0.003893   |     250     
       J Q         |   0.012066   |   0.012331   |     792     
       J K         |   0.012066   |   0.011973   |     769     
       J A         |   0.012066   |   0.012378   |     795     
       Q Q         |   0.004525   |   0.004437   |     285     
       Q K         |   0.012066   |   0.012082   |     776     
       Q A         |   0.012066   |   0.011693   |     751     
       K K         |   0.004525   |   0.004375   |     281     
       K A         |   0.012066   |   0.011787   |     757     
       A A         |   0.004525   |   0.004235   |     272     
---------------------------------------------------------------
       Sum         |   1.000000   |   1.000000   |    64226    
```

## Interpreting Results

Above in the sample output, it was found the "high card" and "pair" sample values were not within the lower and upper values of the 99.7% confidence interval. The high card sample value was below the lower, and the pair sample value was above the upper. This means these that sample values fall within 0.3% of the expected outcomes given the current sample size, which is extremely unusual but not completely impossible. More samples are needed to reach a conclusion.

All other outputs including seem reasonable.

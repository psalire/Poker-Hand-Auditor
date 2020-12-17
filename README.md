
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

On Bovada, you have to manually download hand history for each game in the accounts tab of the client. It then saves the hand history on Windows to `C:\Users\username\Bovada.lv Poker\Hand History\`.

Parsing is only supported for Bovada hand history currently. To add parsing for other sites, create a new class in `Parse.py` with same methods as class `Bovada`.

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
> python main.py "C:\Users\psalire\Bovada.lv Poker\Hand History\012345678910" --stdev 3

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
```

## Interpreting Results

Above in the sample output, it was found the "high card" and "pair" sample values were not within the lower and upper values of the 99.7% confidence interval. The high card sample value was below the lower, and the pair sample value was above the upper. This means these sample values fall within 0.3% of the expected outcomes given the current sample size, which is extremely unusual but not completely impossible. More samples are needed to reach a conclusion.


# Poker Hand Auditor (with Confidence Intervals)

Calculate proportion of card draws and hands compared to the expected values with confidence limits. These are the same methods as shown in iTechlabs' [example audit report](https://itechlabs.com/certification-services/rtprng-audits/), which is the leader in RNG audits for casinos.

iTechlabs also uses Marsaglia's "diehard" tests which are not covered in this script.

## How it works

It parses hand history files for hole cards and board cards while counting every drawn card, and all combinations of 5-card hands and their ranks (e.g. pair, straight, etc.) between the hole cards and board cards. etc. Final output is two tables of the found sample proportions and upper and lower confidence limits, one for card frequency and one for hand frequency.

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
usage: main.py [-h] [--onlyme] [--stdev {1,2,3}] [--site {Bovada}] path

Poker Hand Auditor

positional arguments:
  path             Path to hand history directory

optional arguments:
  -h, --help       show this help message and exit
  --onlyme         Only count my hands
  --stdev {1,2,3}  Stdev for confidence limit, so 1 for 68%, 2 for 95%, and 3
                   for 99.7%. Default=2
  --site {Bovada}  Which site's hand history is being parsed. Default=Bovada

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
---------------------------------------------------------------------------------------------
                   Distribution of Cards, 99.7% Confidence Limit, n=154740                   
---------------------------------------------------------------------------------------------
       Card        |   Expected   |    Sample    |    Lower     |    Upper     |     Size    
---------------------------------------------------------------------------------------------
        2c         |   0.019231   |   0.019426   |   0.011716   |   0.026745   |     3006    
        2d         |   0.019231   |   0.018676   |   0.011567   |   0.026895   |     2890    
        2h         |   0.019231   |   0.019187   |   0.011669   |   0.026792   |     2969    
        2s         |   0.019231   |   0.019736   |   0.011775   |   0.026686   |     3054    
        3c         |   0.019231   |   0.019329   |   0.011697   |   0.026764   |     2991    
        3d         |   0.019231   |   0.018922   |   0.011617   |   0.026845   |     2928    
        3h         |   0.019231   |   0.018864   |   0.011605   |   0.026857   |     2919    
        3s         |   0.019231   |   0.019368   |   0.011705   |   0.026757   |     2997    
        4c         |   0.019231   |   0.019310   |   0.011694   |   0.026768   |     2988    
        4d         |   0.019231   |   0.019284   |   0.011688   |   0.026773   |     2984    
        4h         |   0.019231   |   0.019349   |   0.011701   |   0.026760   |     2994    
        4s         |   0.019231   |   0.019058   |   0.011644   |   0.026818   |     2949    
        5c         |   0.019231   |   0.019685   |   0.011766   |   0.026696   |     3046    
        5d         |   0.019231   |   0.019362   |   0.011704   |   0.026758   |     2996    
        5h         |   0.019231   |   0.019219   |   0.011676   |   0.026786   |     2974    
        5s         |   0.019231   |   0.019381   |   0.011707   |   0.026754   |     2999    
        6c         |   0.019231   |   0.019568   |   0.011743   |   0.026718   |     3028    
        6d         |   0.019231   |   0.019646   |   0.011758   |   0.026703   |     3040    
        6h         |   0.019231   |   0.018857   |   0.011604   |   0.026858   |     2918    
        6s         |   0.019231   |   0.019581   |   0.011746   |   0.026716   |     3030    
        7c         |   0.019231   |   0.019297   |   0.011691   |   0.026771   |     2986    
        7d         |   0.019231   |   0.018857   |   0.011604   |   0.026858   |     2918    
        7h         |   0.019231   |   0.019232   |   0.011678   |   0.026783   |     2976    
        7s         |   0.019231   |   0.019122   |   0.011657   |   0.026805   |     2959    
        8c         |   0.019231   |   0.019174   |   0.011667   |   0.026795   |     2967    
        8d         |   0.019231   |   0.019284   |   0.011688   |   0.026773   |     2984    
        8h         |   0.019231   |   0.019064   |   0.011645   |   0.026816   |     2950    
        8s         |   0.019231   |   0.019691   |   0.011767   |   0.026695   |     3047    
        9c         |   0.019231   |   0.018922   |   0.011617   |   0.026845   |     2928    
        9d         |   0.019231   |   0.019200   |   0.011672   |   0.026790   |     2971    
        9h         |   0.019231   |   0.020027   |   0.011830   |   0.026632   |     3099    
        9s         |   0.019231   |   0.019025   |   0.011637   |   0.026824   |     2944    
        Tc         |   0.019231   |   0.019193   |   0.011671   |   0.026791   |     2970    
        Td         |   0.019231   |   0.019174   |   0.011667   |   0.026795   |     2967    
        Th         |   0.019231   |   0.019168   |   0.011666   |   0.026796   |     2966    
        Ts         |   0.019231   |   0.019607   |   0.011751   |   0.026711   |     3034    
        Jc         |   0.019231   |   0.018896   |   0.011611   |   0.026850   |     2924    
        Jd         |   0.019231   |   0.019232   |   0.011678   |   0.026783   |     2976    
        Jh         |   0.019231   |   0.019148   |   0.011662   |   0.026800   |     2963    
        Js         |   0.019231   |   0.019265   |   0.011685   |   0.026777   |     2981    
        Qc         |   0.019231   |   0.018735   |   0.011579   |   0.026883   |     2899    
        Qd         |   0.019231   |   0.018689   |   0.011569   |   0.026892   |     2892    
        Qh         |   0.019231   |   0.019226   |   0.011677   |   0.026784   |     2975    
        Qs         |   0.019231   |   0.019710   |   0.011771   |   0.026691   |     3050    
        Kc         |   0.019231   |   0.019239   |   0.011680   |   0.026782   |     2977    
        Kd         |   0.019231   |   0.019471   |   0.011725   |   0.026737   |     3013    
        Kh         |   0.019231   |   0.019155   |   0.011663   |   0.026798   |     2964    
        Ks         |   0.019231   |   0.019329   |   0.011697   |   0.026764   |     2991    
        Ac         |   0.019231   |   0.018903   |   0.011613   |   0.026849   |     2925    
        Ad         |   0.019231   |   0.018948   |   0.011622   |   0.026840   |     2932    
        Ah         |   0.019231   |   0.018922   |   0.011617   |   0.026845   |     2928    
        As         |   0.019231   |   0.019284   |   0.011688   |   0.026773   |     2984    
---------------------------------------------------------------------------------------------
       Sum         |   1.000000   |   1.000000   |   0.607226   |   1.392774   |    154740   

```

## Interpreting Results

The sample proportion should generally be within the lower and upper values.

Above in the sample output, it was found the high card and pair sample values were not within the lower and upper values of the 99.7% confidence interval. The high card sample value was below the lower, and the pair sample value was above the upper. This means these sample values fall within 0.3% of the expected outcomes given the current sample size, which is extremely unusual but not completely impossible. More samples are needed to reach a conclusion.

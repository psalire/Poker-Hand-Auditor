
# Poker Hand Auditor

This script takes a user's poker hand history and calculates proportions of card draws and hands compared to the expected values, their confidence intervals, and chi-square p-values to determine if the site's RNG is behaving as expected. These are some of the same methods as shown in iTechlabs' [example audit report](https://itechlabs.com/certification-services/rtprng-audits/), who are one of the leaders in RNG audits for casinos. See iTechlabs' [audits for Partypoker](https://www.partypoker.com/en/s/systemfairness) for an actual audit report.

iTechlabs also uses Marsaglia's "diehard" tests which are not covered in this script but worth looking into.

## How it works

[Proportion of poker hands](https://en.wikipedia.org/wiki/Poker_probability):

| Hand       | High Card | Pair  | Two Pair | Trips | Straight | Flush | Full House | Quads  | Straight Flush |
|------------|-----------|-------|----------|-------|----------|-------|------------|--------|----------------|
| Proportion | 0.501     | 0.423 | 0.048    | 0.021 | 0.004    | 0.002 | 0.001      | 0.0002 | 0.00003        |

A good, genuine RNG will produce these proportions given a significantly large sample size. Smaller sample sizes should fit within a reasonable confidence interval. In addition, the proportion of individual cards and hole cards (not counting suits) should be uniform distributions.

This script parses hand history files for hole and board cards and counts every drawn card, and all 5-card hands and their ranks (e.g. pair, straight, etc.). Optionally, also counts the hole card distribution and/or the distribution of all hand combinations of hole and board cards.

Final output is tables of the sample proportions compared to the expected with upper and lower confidence limits and chi-square goodness of fit test results.

## Dependencies

- Python 3 (3.9.1)
- treys - [A poker hand evaluation library](https://github.com/ihendley/treys)
    - `python -m pip install treys`
- scipy - For chi-square tests
    - `python -m pip install scipy matplotlib ipython jupyter pandas sympy nose numpy==1.19.3`

## Files

```
main.py  - Main script for output
Parse.py - Parsing hand history files
Results.py - Computing and printing results
```

## How to use

Locate the directory where your poker client saves hand history. Run with `python main.py "C:\path\to\your\hand_history"`. See usage below for more options.

### Site Support

Parsing is only supported for Bovada hand history currently. To add parsing for other sites, create a new class in `Parse.py` with same methods as class `Bovada`.

On Bovada, you have to manually download hand history for each game under the "Account > Hand History > Game Transactions" tabs of the client. It then saves the hand history on Windows to `C:\Users\username\Bovada.lv Poker\Hand History\`.

### Usage

```
usage: main.py [-h] [--site {Bovada}] [--summaryonly] [--stdev {1,2,3}]
               [--bins BINS] [--showallbinnedtables] [--onlyme] [--holecards]
               [--holecardswithsuits] [--allcombinations]
               path

This script takes a user's poker hand history and calculates proportions of
card draws and hands compared to the expected values, their confidence
intervals, and chi-square p-values to determine if the site's RNG is behaving
as expected.

positional arguments:
  path                  Path to hand history directory

optional arguments:
  -h, --help            show this help message and exit
  --site {Bovada}       Which site's hand history is being parsed.
                        Default=Bovada
  --summaryonly         Show summary only, no tables.
  --stdev {1,2,3}       Stdev for confidence limit, so 1 for 68%, 2 for 95%,
                        and 3 for 99.7%. Default=2
  --bins BINS           Number of bins for p-value uniformity test
                        (Kolmogorov-Smirnov test on Chi-square p-values).
                        Default=10
  --showallbinnedtables
                        Show tables for all bins.
  --onlyme              Only count my hands
  --holecards           Show results for frequency of hole cards without suits
  --holecardswithsuits  Show results for frequency of hole cards with suits
                        (Long output)
  --allcombinations     Show results for frequency of all combinations between
                        hole and board cards.
```

### Sample output

```
> python main.py "C:\Users\psalire\Bovada.lv Poker\Hand History\012345678910" --stdev 3 --allcombinations --holecards

---------------------------------------------------------------------------------------------------------------
                          Distribution of All Hands, 99.7% Confidence Level, n=45276                           |
---------------------------------------------------------------------------------------------------------------
     Hand      |   Expected    | Expected Size |    Sample     |     Lower     |     Upper     |  Sample Size  |
---------------------------------------------------------------------------------------------------------------
   high card   |   0.501177    |     22691     |   0.284787    |   0.487967    |   0.514387    |     12894     |
     pair      |   0.422569    |     19132     |   0.440388    |   0.412074    |   0.433064    |     19939     |
   two pair    |   0.047539    |     2152      |   0.167064    |   0.040199    |   0.054879    |     7564      |
three of a kind|   0.021128    |      957      |   0.038630    |   0.010812    |   0.031444    |     1749      |
   straight    |   0.003925    |      178      |   0.031297    |   -0.001058   |   0.008908    |     1417      |
     flush     |   0.001965    |      89       |   0.020629    |   -0.002382   |   0.006312    |      934      |
  full house   |   0.001441    |      65       |   0.015726    |   -0.002824   |   0.005706    |      712      |
four of a kind |   0.000240    |      11       |   0.001281    |   -0.005862   |   0.006342    |      58       |
straight flush |   0.000015    |       1       |   0.000199    |   -0.003914   |   0.003945    |       9       |
---------------------------------------------------------------------------------------------------------------
     Total     |   0.999999    |     45276     |   1.000000    |   0.935013    |   1.064986    |     45276     |
---------------------------------------------------------------------------------------------------------------
                                        Chi-Square Goodness of Fit Test                                        |
---------------------------------------------------------------------------------------------------------------
                      Chi-square                       |                     41881.872777                      |
                  Chi-square p-value                   |                       0.000000                        |
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------
          Chi-square p-values of binned Distribution of Hands, n=45276           |
---------------------------------------------------------------------------------
                  Bin                   |                p-value                 |
---------------------------------------------------------------------------------
                   0                    |                0.000000                |
                   1                    |                0.000000                |
                   2                    |                0.000000                |
                   3                    |                0.000000                |
                   4                    |                0.000000                |
                   5                    |                0.000000                |
                   6                    |                0.000000                |
                   7                    |                0.000000                |
                   8                    |                0.000000                |
                   9                    |                0.000000                |
---------------------------------------------------------------------------------
            Kolmogorov-Smirnov uniformity test of Chi-square p-values            |
---------------------------------------------------------------------------------
                   KS                   |                1.000000                |
                p-value                 |                0.000000                |
---------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------------
                   Distribution of Hands, All Combinations, 99.7% Confidence Level, n=590856                   |
---------------------------------------------------------------------------------------------------------------
     Hand      |   Expected    | Expected Size |    Sample     |     Lower     |     Upper     |  Sample Size  |
---------------------------------------------------------------------------------------------------------------
   high card   |   0.501177    |    296123     |   0.494642    |   0.498402    |   0.503952    |    292262     |
     pair      |   0.422569    |    249677     |   0.427201    |   0.419619    |   0.425519    |    252414     |
   two pair    |   0.047539    |     28089     |   0.048519    |   0.043769    |   0.051309    |     28668     |
three of a kind|   0.021128    |     12484     |   0.021467    |   0.017297    |   0.024959    |     12684     |
   straight    |   0.003925    |     2319      |   0.004194    |   0.000157    |   0.007693    |     2478      |
     flush     |   0.001965    |     1161      |   0.002222    |   -0.001701   |   0.005631    |     1313      |
  full house   |   0.001441    |      851      |   0.001472    |   -0.002417   |   0.005299    |      870      |
four of a kind |   0.000240    |      142      |   0.000266    |   -0.003469   |   0.003949    |      157      |
straight flush |   0.000015    |       9       |   0.000017    |   -0.003712   |   0.003743    |      10       |
---------------------------------------------------------------------------------------------------------------
     Total     |   0.999999    |    590855     |   1.000000    |   0.967945    |   1.032054    |    590856     |
---------------------------------------------------------------------------------------------------------------
                                        Chi-Square Goodness of Fit Test                                        |
---------------------------------------------------------------------------------------------------------------
                      Chi-square                       |                      128.405743                       |
                  Chi-square p-value                   |                       0.000000                        |
---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------
 Chi-square p-values of binned Distribution of Hands, All Combinations, n=590856 |
---------------------------------------------------------------------------------
                  Bin                   |                p-value                 |
---------------------------------------------------------------------------------
                   0                    |                0.000000                |
                   1                    |                0.000204                |
                   2                    |                0.008364                |
                   3                    |                0.000000                |
                   4                    |                0.000000                |
                   5                    |                0.003877                |
                   6                    |                0.004752                |
                   7                    |                0.000000                |
                   8                    |                0.002906                |
                   9                    |                0.000000                |
---------------------------------------------------------------------------------
            Kolmogorov-Smirnov uniformity test of Chi-square p-values            |
---------------------------------------------------------------------------------
                   KS                   |                0.991636                |
                p-value                 |                0.000000                |
---------------------------------------------------------------------------------

-------------------------------------------------------------------------------
                        Distribution of Cards, n=160377                        |
-------------------------------------------------------------------------------
     Card      |   Expected    | Expected Size |    Sample     |  Sample Size  |
-------------------------------------------------------------------------------
      2c       |   0.019231    |     3084      |   0.019373    |     3107      |
      2d       |   0.019231    |     3084      |   0.018750    |     3007      |
      2h       |   0.019231    |     3084      |   0.019180    |     3076      |
      2s       |   0.019231    |     3084      |   0.019753    |     3168      |
      3c       |   0.019231    |     3084      |   0.019342    |     3102      |
      3d       |   0.019231    |     3084      |   0.018968    |     3042      |
      3h       |   0.019231    |     3084      |   0.018899    |     3031      |
      3s       |   0.019231    |     3084      |   0.019392    |     3110      |
      4c       |   0.019231    |     3084      |   0.019248    |     3087      |
      4d       |   0.019231    |     3084      |   0.019305    |     3096      |
      4h       |   0.019231    |     3084      |   0.019286    |     3093      |
      4s       |   0.019231    |     3084      |   0.019036    |     3053      |
      5c       |   0.019231    |     3084      |   0.019647    |     3151      |
      5d       |   0.019231    |     3084      |   0.019329    |     3100      |
      5h       |   0.019231    |     3084      |   0.019161    |     3073      |
      5s       |   0.019231    |     3084      |   0.019361    |     3105      |
      6c       |   0.019231    |     3084      |   0.019579    |     3140      |
      6d       |   0.019231    |     3084      |   0.019666    |     3154      |
      6h       |   0.019231    |     3084      |   0.018881    |     3028      |
      6s       |   0.019231    |     3084      |   0.019566    |     3138      |
      7c       |   0.019231    |     3084      |   0.019336    |     3101      |
      7d       |   0.019231    |     3084      |   0.018862    |     3025      |
      7h       |   0.019231    |     3084      |   0.019236    |     3085      |
      7s       |   0.019231    |     3084      |   0.019174    |     3075      |
      8c       |   0.019231    |     3084      |   0.019136    |     3069      |
      8d       |   0.019231    |     3084      |   0.019223    |     3083      |
      8h       |   0.019231    |     3084      |   0.019074    |     3059      |
      8s       |   0.019231    |     3084      |   0.019672    |     3155      |
      9c       |   0.019231    |     3084      |   0.019043    |     3054      |
      9d       |   0.019231    |     3084      |   0.019273    |     3091      |
      9h       |   0.019231    |     3084      |   0.019953    |     3200      |
      9s       |   0.019231    |     3084      |   0.019055    |     3056      |
      Tc       |   0.019231    |     3084      |   0.019136    |     3069      |
      Td       |   0.019231    |     3084      |   0.019211    |     3081      |
      Th       |   0.019231    |     3084      |   0.019217    |     3082      |
      Ts       |   0.019231    |     3084      |   0.019654    |     3152      |
      Jc       |   0.019231    |     3084      |   0.018937    |     3037      |
      Jd       |   0.019231    |     3084      |   0.019223    |     3083      |
      Jh       |   0.019231    |     3084      |   0.019199    |     3079      |
      Js       |   0.019231    |     3084      |   0.019248    |     3087      |
      Qc       |   0.019231    |     3084      |   0.018718    |     3002      |
      Qd       |   0.019231    |     3084      |   0.018625    |     2987      |
      Qh       |   0.019231    |     3084      |   0.019211    |     3081      |
      Qs       |   0.019231    |     3084      |   0.019641    |     3150      |
      Kc       |   0.019231    |     3084      |   0.019248    |     3087      |
      Kd       |   0.019231    |     3084      |   0.019373    |     3107      |
      Kh       |   0.019231    |     3084      |   0.019192    |     3078      |
      Ks       |   0.019231    |     3084      |   0.019342    |     3102      |
      Ac       |   0.019231    |     3084      |   0.018899    |     3031      |
      Ad       |   0.019231    |     3084      |   0.018937    |     3037      |
      Ah       |   0.019231    |     3084      |   0.018943    |     3038      |
      As       |   0.019231    |     3084      |   0.019286    |     3093      |
-------------------------------------------------------------------------------
     Total     |   1.000000    |    160368     |   1.000000    |    160377     |
-------------------------------------------------------------------------------
                        Chi-Square Goodness of Fit Test                        |
-------------------------------------------------------------------------------
              Chi-square               |               32.552205               |
          Chi-square p-value           |               0.979386                |
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
               Distribution of Hole Cards without suits, n=66524               |
-------------------------------------------------------------------------------
  Hole Cards   |   Expected    | Expected Size |    Sample     |  Sample Size  |
-------------------------------------------------------------------------------
      2 2      |   0.004525    |      301      |   0.004374    |      291      |
      2 3      |   0.012066    |      803      |   0.011996    |      798      |
      2 4      |   0.012066    |      803      |   0.011755    |      782      |
      2 5      |   0.012066    |      803      |   0.012822    |      853      |
      2 6      |   0.012066    |      803      |   0.012221    |      813      |
      2 7      |   0.012066    |      803      |   0.012101    |      805      |
      2 8      |   0.012066    |      803      |   0.012251    |      815      |
      2 9      |   0.012066    |      803      |   0.012477    |      830      |
      2 T      |   0.012066    |      803      |   0.012251    |      815      |
      2 J      |   0.012066    |      803      |   0.012251    |      815      |
      2 Q      |   0.012066    |      803      |   0.011725    |      780      |
      2 K      |   0.012066    |      803      |   0.012642    |      841      |
      2 A      |   0.012066    |      803      |   0.011409    |      759      |
      3 3      |   0.004525    |      301      |   0.004374    |      291      |
      3 4      |   0.012066    |      803      |   0.012266    |      816      |
      3 5      |   0.012066    |      803      |   0.012086    |      804      |
      3 6      |   0.012066    |      803      |   0.012567    |      836      |
      3 7      |   0.012066    |      803      |   0.012522    |      833      |
      3 8      |   0.012066    |      803      |   0.011560    |      769      |
      3 9      |   0.012066    |      803      |   0.011439    |      761      |
      3 T      |   0.012066    |      803      |   0.012236    |      814      |
      3 J      |   0.012066    |      803      |   0.011424    |      760      |
      3 Q      |   0.012066    |      803      |   0.011875    |      790      |
      3 K      |   0.012066    |      803      |   0.012026    |      800      |
      3 A      |   0.012066    |      803      |   0.011755    |      782      |
      4 4      |   0.004525    |      301      |   0.004810    |      320      |
      4 5      |   0.012066    |      803      |   0.011905    |      792      |
      4 6      |   0.012066    |      803      |   0.011439    |      761      |
      4 7      |   0.012066    |      803      |   0.011815    |      786      |
      4 8      |   0.012066    |      803      |   0.011635    |      774      |
      4 9      |   0.012066    |      803      |   0.011515    |      766      |
      4 T      |   0.012066    |      803      |   0.011710    |      779      |
      4 J      |   0.012066    |      803      |   0.012341    |      821      |
      4 Q      |   0.012066    |      803      |   0.012101    |      805      |
      4 K      |   0.012066    |      803      |   0.012131    |      807      |
      4 A      |   0.012066    |      803      |   0.012236    |      814      |
      5 5      |   0.004525    |      301      |   0.004179    |      278      |
      5 6      |   0.012066    |      803      |   0.011665    |      776      |
      5 7      |   0.012066    |      803      |   0.011875    |      790      |
      5 8      |   0.012066    |      803      |   0.012356    |      822      |
      5 9      |   0.012066    |      803      |   0.011966    |      796      |
      5 T      |   0.012066    |      803      |   0.012311    |      819      |
      5 J      |   0.012066    |      803      |   0.012296    |      818      |
      5 Q      |   0.012066    |      803      |   0.011981    |      797      |
      5 K      |   0.012066    |      803      |   0.012837    |      854      |
      5 A      |   0.012066    |      803      |   0.012266    |      816      |
      6 6      |   0.004525    |      301      |   0.004239    |      282      |
      6 7      |   0.012066    |      803      |   0.011770    |      783      |
      6 8      |   0.012066    |      803      |   0.012657    |      842      |
      6 9      |   0.012066    |      803      |   0.012041    |      801      |
      6 T      |   0.012066    |      803      |   0.012356    |      822      |
      6 J      |   0.012066    |      803      |   0.012236    |      814      |
      6 Q      |   0.012066    |      803      |   0.011515    |      766      |
      6 K      |   0.012066    |      803      |   0.012552    |      835      |
      6 A      |   0.012066    |      803      |   0.013033    |      867      |
      7 7      |   0.004525    |      301      |   0.004540    |      302      |
      7 8      |   0.012066    |      803      |   0.012011    |      799      |
      7 9      |   0.012066    |      803      |   0.011936    |      794      |
      7 T      |   0.012066    |      803      |   0.012086    |      804      |
      7 J      |   0.012066    |      803      |   0.012176    |      810      |
      7 Q      |   0.012066    |      803      |   0.012356    |      822      |
      7 K      |   0.012066    |      803      |   0.012086    |      804      |
      7 A      |   0.012066    |      803      |   0.011439    |      761      |
      8 8      |   0.004525    |      301      |   0.004359    |      290      |
      8 9      |   0.012066    |      803      |   0.012371    |      823      |
      8 T      |   0.012066    |      803      |   0.012356    |      822      |
      8 J      |   0.012066    |      803      |   0.012026    |      800      |
      8 Q      |   0.012066    |      803      |   0.012567    |      836      |
      8 K      |   0.012066    |      803      |   0.011725    |      780      |
      8 A      |   0.012066    |      803      |   0.012311    |      819      |
      9 9      |   0.004525    |      301      |   0.004450    |      296      |
      9 T      |   0.012066    |      803      |   0.011830    |      787      |
      9 J      |   0.012066    |      803      |   0.012236    |      814      |
      9 Q      |   0.012066    |      803      |   0.012552    |      835      |
      9 K      |   0.012066    |      803      |   0.012417    |      826      |
      9 A      |   0.012066    |      803      |   0.012522    |      833      |
      T T      |   0.004525    |      301      |   0.004600    |      306      |
      T J      |   0.012066    |      803      |   0.012026    |      800      |
      T Q      |   0.012066    |      803      |   0.011289    |      751      |
      T K      |   0.012066    |      803      |   0.012356    |      822      |
      T A      |   0.012066    |      803      |   0.012131    |      807      |
      J J      |   0.004525    |      301      |   0.003923    |      261      |
      J Q      |   0.012066    |      803      |   0.012326    |      820      |
      J K      |   0.012066    |      803      |   0.012086    |      804      |
      J A      |   0.012066    |      803      |   0.012251    |      815      |
      Q Q      |   0.004525    |      301      |   0.004450    |      296      |
      Q K      |   0.012066    |      803      |   0.011951    |      795      |
      Q A      |   0.012066    |      803      |   0.011755    |      782      |
      K K      |   0.004525    |      301      |   0.004359    |      290      |
      K A      |   0.012066    |      803      |   0.011695    |      778      |
      A A      |   0.004525    |      301      |   0.004269    |      284      |
-------------------------------------------------------------------------------
     Total     |   1.000000    |     66547     |   1.000000    |     66524     |
-------------------------------------------------------------------------------
                        Chi-Square Goodness of Fit Test                        |
-------------------------------------------------------------------------------
              Chi-square               |               70.839001               |
          Chi-square p-value           |               0.932371                |
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
                                    SUMMARY                                    |
-------------------------------------------------------------------------------
                      Distribution of All Hands, n=45276                       |
-------------------------------------------------------------------------------
                 Test                  |                Result                 |
-------------------------------------------------------------------------------
  Sample in 99.7% confidence interval  |                 FAIL                  |
       Chi-square p-value > 0.05       |                 FAIL                  |
     KS uniformity p-value > 0.05      |                 FAIL                  |
-------------------------------------------------------------------------------
               Distribution of Hands, All Combinations, n=590856               |
-------------------------------------------------------------------------------
                 Test                  |                Result                 |
-------------------------------------------------------------------------------
  Sample in 99.7% confidence interval  |                 FAIL                  |
       Chi-square p-value > 0.05       |                 FAIL                  |
     KS uniformity p-value > 0.05      |                 FAIL                  |
-------------------------------------------------------------------------------
                        Distribution of Cards, n=160377                        |
-------------------------------------------------------------------------------
                 Test                  |                Result                 |
-------------------------------------------------------------------------------
       Chi-square p-value > 0.05       |                 PASS                  |
-------------------------------------------------------------------------------
               Distribution of Hole Cards without suits, n=66524               |
-------------------------------------------------------------------------------
                 Test                  |                Result                 |
-------------------------------------------------------------------------------
       Chi-square p-value > 0.05       |                 PASS                  |
-------------------------------------------------------------------------------
                              Passing Tests: 2/8                               |
-------------------------------------------------------------------------------
```

## Interpreting Results

Above in the sample output looking at the first table showing the sampled hand distribution, it's clear that the distribution is very irregular. All hands except for four of a kind and straight flush fall significantly outside of the 99.7% confidence interval. In addition, the most common hand by far was a pair, not high card as is expected.

Furthermore, even when taking all combinations of the hole and board cards in the third table, both high card and pair hands fall outside the 99.7% confidence interval; the high card sample is lower than the lower confidence limit and the pair sample is higher than the upper confidence limit.

Chi-square tests also rejects conformity to the expected hand distributions (p < 0.05).

The distribution of individual cards and hole cards however passed the chi-squared tests (p > 0.05), failing to reject conformity to the expected proportions.

The Kolmogorov-Smirnov tests are not really relevant here as almost all p-values of the chi-square values came out to be 0.0.

Overall, this sample shows a bad RNG algorithm. More samples are needed to reach a conclusion.

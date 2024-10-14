# Nutrition Information and Weight

Around 3500 calories equal one pound. To calculate how much weight you are able to gain in one week. Track your eating and macros, calculate your total daily expected expenditure and add the calories you burned from additional activity to your total daily expected expenditure (I should make a script for this). Take the calories you in a day and subtract that by your total daily expected expenditure. This will tell you if you're in a deficit or surplus. Calculate this number for each day in the week and then calculate your weekly deficit/surplus (I should make a script for this). Now with this number divide it by 3500 to calculate how much weight you should have gained for the week. 

I should make a script which does that calculation and then evaluates if you are losing/gaining weight according to the expected model, this would help to see if you are on track with your goals and how accurate the model is. I would do this by doing the calculations specified above, then averaging out the weight and comparing it against last week and checking how far off the weight is to the calculation.

### Some possible issues 
- I should likely calculate the percent error to see how far off it is and depending on that adjust the algorithm/my understanding of my total daily expected expenditure

#### Weighted rolling average 

- I should value the later days in the week more than the earlier days in the week as that is a more accurate measurement of weight. I would do this by calculating a weighted rolling average. The formula is WMA = (W1 * P1 + W2 * P2 + ... + Wn * Pn) / (W1 + W2 + ... + Wn), where

W1, W2, ..., Wn are the weights (n, n-1, ..., 1)
P1, P2, ..., Pn are the weight measurements (most recent to oldest)

##### Example 

Day 1 (most recent): 150
Day 2: 151
Day 3: 149
Day 4: 150
Day 5: 152
Day 6: 151
Day 7: 150
The weights would be 7, 6, 5, 4, 3, 2, 1 (from most recent to oldest).
WMA = (7150 + 6151 + 5149 + 4150 + 3152 + 2151 + 1*150) / (7+6+5+4+3+2+1)
= (1050 + 906 + 745 + 600 + 456 + 302 + 150) / 28
= 4209 / 28
≈ 150.32 pounds


### Possible future features 
It would be interesting to add something like a nutrition evaluation script which would take in your diet information, scrape for information on those products and their nutrition information and calculate how close you are to hitting the goal macro and micro nutrients

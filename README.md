# Wireless City Network Simulation

## Algorithm
1. ***Minimum threshold***
    - 當每位使用者（Car）所連接的基地台（Base）**`不足 65dB`** 時就會進行基地台連接切換
2. ***Best effort***
    - 每位使用者都固定使用 **`最強`** 訊號基地台
3. ***Entropy***
    - 當使用者的**目前的基地台**強度，與最強訊號基地台強度相比 **`小於 25dB`** 時，就會進行切換
4. ***Maximum threshold***
    - 當使用者目前位置的**最強訊號基地台**強度 **`大於 80dB`** 時，就會進行切換


## CityNetwork file
### description
模擬**每台車皆會與基地台連線**的情況
1. 地圖為 10 * 10 格正方形，長度為 2500m
2. 進入點為 4邊36點，進入機率為 Possion(n=1,t=1)、λ=5/min=(1/12)/sec
3. 每個十字入口**移動方向機率**:
    a. 前進:1/2
    b. 迴轉:1/16
    c. 左右轉:各7/32
4. **車速**為:72km/hr=0.02km/sec 

### demo

![](https://i.imgur.com/EL7GLYq.png)

![](https://i.imgur.com/SmsQStn.png)

## CallService file
### description

呈上條件，模擬進入城市後，使用者
1. **連接頻率**
    - average 2 calls per hour
2. **通話時間**
    - Normal distribution
    - average 3 mins per call 
    - sigma is 1

### demo

![](https://i.imgur.com/GA7zrh7.png)

![](https://i.imgur.com/ekr8Gk1.png)

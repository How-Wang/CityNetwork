# Wireless City Network Simulation

## Algorithm
1. ***Minimum threshold***
    - 當每位使用者（Car）所連接的基地台（Base）**`不足 35dB`** 時就會進行基地台連接切換
2. ***Best effort***
    - 每位使用者都固定使用 **`最強`** 訊號基地台
3. ***Entropy***
    - 當使用者的**目前的基地台**強度，與最強訊號基地台強度相比 **`大於 25dB`** 時，就會進行切換
4. ***Maximum threshold***
    - 當使用者目前位置的**最強訊號基地台**強度 **`大於 60dB`** 時，就會進行切換


## CityNetwork file
### description
模擬**每台車皆會與基地台連線**的情況
1. 地圖為 10 * 10 格正方形，長度為 2500m
2. 進入點為 4邊36點，進入機率為 $Possion(n=1,t=1)$、$λ=5/min=(1/12)/sec$
3. 每個十字入口**移動方向機率**:
    a. 前進:$1\over2$
    b. 迴轉:$1\over16$
    c. 左右轉:各$7\over32$
4. **車速**為:$72km/hr=0.02km/sec$ 

### demo
```
python .\CityNetwork.py
> Which algorithm you want (1, 2, 3, 4)?2
> You choose Best effort algorithm
```

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

```
python .\CallService.py
> Which algorithm you want (1, 2, 3, 4)?3
> You choose Entropy algorithm
```

![](https://i.imgur.com/ekr8Gk1.png)

## Algorithm 的比較

1. ***Minimum threshold***
    - :heavy_check_mark:**`優點`**：如果在一個功率附近以下，收訊效果很差，就可以使用這個演算法，進行有效率的切換
    - :x:**`缺點`**：只有考慮到原先基地台的功率但沒有考慮到新的基地台的功率效果
2. ***Entropy***
    - :heavy_check_mark:**`優點`**：成功考慮、並相比原先基地台的功率與後來基地台的功率，所以差距如果不大、效果差不多，就可以不用更換基地台
    - :x:**`缺點`**：如果某些區段功率以上或以下的表現會特別好、特別糟的情況，就沒辦法在這個演算法上面實現調整
3. ***Best effort***
    - :heavy_check_mark:**`優點`**：挑選到最好的極致，接收者功率一定最大、傳輸效果最好
    - :x:**`缺點`**：會消耗最多的能量，造成不必要的浪費
4. ***Maximum threshold***
    - :heavy_check_mark:**`優點`**：如果在一個功率附近以上，收訊效果很好，就可以使用這個演算法，進行有效率的切換
    - :x:**`缺點`**：只有考慮到新基地台的功率但沒有考慮到目前的基地台的功率效果


> 此外 1 3 4 三種演算法都可以根據當地的情況 進行彈性調整，也能因應能源消耗的狀況、改變數值。
 

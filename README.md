# RMK Data Team Internship – Test Challenge 2025  
### 🚌 Bus Delay Analysis for Line 8 (Toompark ↔ Zoo ↔ Aigrumäe)

This small data project was made as part of the RMK internship test challenge. The goal was to explore a real-world dataset and demonstrate my way of thinking statistically and technically.

---

## 🕒 Context

I had only 24 hours to track and analyze the bus delays. The dataset comes from bus line number 8 (Toompark–Aigrumäe), and it covers about one full day of observations.  

Due to server errors, I wasn’t able to log every single event, but I still managed to record **94 valid arrival timestamps** and calculate the delay for each one based on the official schedule.

---

## 📊 What I Did

- Parsed GPS logs with timestamps and matched them to scheduled bus departures from Zoo and Toompark
- Calculated delays in **seconds**, comparing real timestamps to closest scheduled departure
- Calculated basic statistics and delay probabilities

---

## 🧮 Results

| Delay Category | Count | Probability |
|----------------|-------|-------------|
| Early          | 3     | 3.23%        |
| On Time        | 33    | 35.48%       |
| Late           | 57    | 61.29%       |

Ritas probablity to arrived on time mattered only how often the nr 8 bus on its way to Aigrumäe was late. 

If Rita leaves home 8:32 there is 100% chance that she is on time. As it takes her to walk to the bus station 5 minutes and probably some seconds to get onto the bus. So she gets onto the 8:38 bus which according to my data cant be too late. 

If Rita leaves home between 8:33 and 8:42 there is 61.29% probability that she will be late. As the bus that departs from 8:48 has to be on time even if the bus is late 1 second then Rita is late already. 

Obviously there are many other factors that can change the probability but this time i only took into account the probability of how much Rita is late. 


---

## 📁 Files in This Project

- `analyze_delays.py` – main script that parses raw data and calculates delay
- `analyze_probabilities.py` – computes probability stats based on cleaned output
- `bus_delay_analysis.csv` – final dataset used for stats

---

## 🛠️ Tech Used

- Python  
- Pandas for data manipulation  

---

## 🧠 What I’d Add Next (with more time)


- Deploy the graph showing the probabilities 
- Use more days of tracking and cover other routes  

---

## ✍️ Author

Siim Kiskonen  

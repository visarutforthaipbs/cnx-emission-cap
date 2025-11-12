# C-CAX MVP: Cap Calculator Methodology

## 1. Objective

The goal of this model is to calculate the **Daily Emission Cap** (the "Cap") for the Chiang Mai-Lamphun basin. The "Cap" represents the maximum amount of PM2.5 (in **Tons/Day**) that can be emitted into the atmosphere while ensuring the average air quality remains at or below the Thai national standard (37.5 µg/m³).

## 2. The Scientific Model: Steady-State Box Model

Our methodology is based on a standard, scientifically-defensible approach called the **"Steady-State Box Model."**

This model treats the Chiang Mai-Lamphun basin as a simple "Box." We calculate the maximum amount of pollution we can put _into_ the box by calculating how fast the wind flushes the pollution _out_ of it.

The core assumption is: **Emissions In = Pollutants Flushed Out**

## 3. The Core Formula

The model solves for **Q** (the "Cap") using the following formula:

$$Q = \frac{C \cdot V}{\tau}$$

Where:

- **Q = Emission Rate "Cap"** (Mass/Time)
  - _This is our answer (e.g., in Tons/Day)._
- **C = Target Concentration** (Mass/Volume)
  - _Our defined air quality goal._
- **V = Volume of the Box** (Volume)
  - _The "size" of the air in the basin, which changes daily._
- **$\tau$ (Tau) = Residence Time** (Time)
  - _The average time it takes for air to be flushed out of the box._

---

## 4. Step-by-Step Calculation

Here is how the script (`cap_calculator.py`) calculates the Cap every day.

### Step 1: Define Static Constants

These are the fixed numbers that define our "Box" geometry and goals.

- **C (Target Concentration):**
  - **Value:** `37.5` µg/m³
  - _Why:_ The Thai national 24-hour standard for PM2.5.
- **A (Basin Area):**
  - **Value:** `1,600,000,000` m² (1,600 km²)
  - _Why:_ Our GIS-based estimate of the basin's "floor."
- **L (Basin Length):**
  - **Value:** `80,000` m (80 km)
  - _Why:_ The approximate N-S length used to calculate flushing time.
- **K (Conversion Factor):**
  - **Value:** `8.64e-8`
  - _Why:_ A constant to convert `µg/s` (micrograms/second) to `Tons/Day`.

### Step 2: Fetch Dynamic Variables (via API)

This data changes every day. The script calls the **Open-Meteo API** for a 24-hour forecast.

- **H (Mixing Height):**
  - **Source:** The API parameter `blh` (Boundary Layer Height) in meters.
  - **Logic:** We fetch all 24 hourly values for tomorrow and calculate the **24-hour average**.
- **U (Wind Speed):**
  - **Source:** The API parameter `wind_speed_10m` in km/h.
  - **Logic:** We fetch all 24 hourly values, convert them to `m/s`, and calculate the **24-hour average**.

### Step 3: Calculate Intermediate Variables

The script uses the data from Steps 1 & 2 to find **V** and **$\tau$**.

- **To Find V (Volume):**
  - **Formula:** `V = A * H`
  - **Example:** `1,600,000,000 m² * 332.3 m (Avg. Height)` = `5.3e11 m³`
- **To Find $\tau$ (Residence Time):**
  - **Formula:** `$\tau$ = L / U`
  - **Example:** `80,000 m / 0.8 m/s (Avg. Wind)` = `100,000 seconds` (~27.8 hours)

### Step 4: Solve for Q (The Cap)

The script now has every number it needs to solve the main formula.

1.  **Solve for Q in µg/s:**

    - **Formula:** `Q = (C * V) / $\tau$`
    - **Example:** `(37.5 * 5.3e11) / 100,000` = `187,500,000 µg/s`

2.  **Convert to Tons/Day:**
    - **Formula:** `Cap = Q (in µg/s) * K`
    - **Example:** `187,500,000 * 8.64e-8` = **`16.15 Tons/Day`**

This final number is the "Daily Emission Cap."

---

## 5. Key Assumptions & Methodological Weaknesses

This MVP is powerful but relies on simplifications. The methodology's weakest points are:

1.  **Plug Flow ($\tau$):** We assume air moves like a solid "plug." The reality is complex, with swirls and dead zones. This is the biggest scientific simplification.
2.  **Box Geometry ($V$):** We assume the basin is a flat-bottomed box. It's really a V-shaped valley, meaning our Volume ($V$) is likely _overestimated_ on low-height days.
3.  **24-Hour Averaging ($H$, $U$):** We average the day's weather. This hides the dangerous morning "inversion" when the _real_ cap is near-zero, but traffic and activity are high.

Despite these weaknesses, this model is a robust and scientifically-sound MVP that successfully links atmospheric carrying capacity to a quantitative, daily "Cap."

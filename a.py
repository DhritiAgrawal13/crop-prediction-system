# import streamlit as st
# import pickle
# import numpy as np
# import requests
# from google import genai

# with open("crop_model.pkl", "rb") as f:
#     model = pickle.load(f)

# with open("scaler.pkl", "rb") as f:
#     scaler = pickle.load(f)

# district_map = {
#     "Ranchi": 0,
#     "Dhanbad": 1,
#     "Hazaribagh": 2,
#     "Bokaro": 3
# }

# soil_map = {
#     "Loamy": 0,
#     "Clay": 1,
#     "Sandy": 2
# }

# def get_weather_data(city):
#     url = f"http://api.weatherapi.com/v1/current.json?key=d2acf64e8b6e4288b58122130250712&q={city}&aqi=no"
#     res = requests.get(url).json()
#     temperature = res['current']['temp_c']
#     humidity = res['current']['humidity']
#     rainfall = res.get("rain", {}).get("1h", 0)
#     solar_radiation = 18
#     return temperature, rainfall, humidity, solar_radiation

# def get_soil_data(district):
#     return {
#         "N": 90,
#         "P": 40,
#         "K": 45,
#         "soil_ph": 6.5,
#         "soil_moisture": 38
#     }

# def get_water_data(district):
#     return {
#         "water_ph": 7.2,
#         "water_ec": 0.9,
#         "water_tds": 520,
#         "water_salinity": 0.3,
#         "water_hardness": 180
#     }

# def get_agri_recommendation(crop_name, soil, water, weather):
#     client = genai.Client(api_key="AIzaSyDntg7SvuWJTAoTrz2mauytNexukMp5JBQ")
#     prompt = f"""
#     Provide JSON with keys fertilizer, pesticide, irrigation for:
#     Crop: {crop}, Soil: {soil}, Water: {water}, Weather: {weather}
#     """
#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=prompt
#     )
#     json_text = response['choices'][0]['message']['content'].strip()
#     return json_text

# def predict_crop(district, soil_type, season):
#     district_encoded = district_map[district]
#     soil_encoded = soil_map[soil_type]
#     temperature, rainfall, humidity, solar = get_weather_data(district)
#     soil = get_soil_data(district)
#     water = get_water_data(district)
#     features = np.array([[
#         district_encoded,
#         soil_encoded,
#         soil["N"],
#         soil["P"],
#         soil["K"],
#         soil["soil_ph"],
#         soil["soil_moisture"],
#         water["water_ph"],
#         water["water_ec"],
#         water["water_tds"],
#         water["water_salinity"],
#         water["water_hardness"],
#         temperature,
#         rainfall,
#         humidity,
#         solar
#     ]])
#     features_scaled = scaler.transform(features)
#     prediction = model.predict(features_scaled)
#     crop_name = prediction[0]
#     weather_data = {
#         "temperature": temperature,
#         "rainfall": rainfall,
#         "humidity": humidity,
#         "solar_radiation": solar
#     }
#     agri_json = get_agri_recommendation(crop_name, soil, water, weather_data)
#     return crop_name, agri_json

# st.set_page_config(page_title="AI Crop & Fertilizer Predictor", page_icon="🌾")
# st.title(" AI-Based Crop Prediction & Recommendation System")
# st.write("Predict crop and get fertilizer, pesticide & irrigation recommendation in JSON format.")

# district = st.selectbox("Select District", list(district_map.keys()))
# soil_type = st.selectbox("Select Soil Type", list(soil_map.keys()))
# season = st.selectbox("Select Season", ["Kharif", "Rabi", "Zaid"])

# if st.button("Predict & Recommend "):
#     with st.spinner("Predicting crop and fetching recommendations..."):
#         crop, recommendations = predict_crop(district, soil_type, season)
#     st.success(f"🌾 Predicted Crop: {crop}")
#     st.json(recommendations)
#     st.info("Recommendations are fetched from Google AI API in JSON format.")
import streamlit as st
import pickle
import numpy as np
import requests
import json
import time
import random
from google import genai
from google.genai.errors import ServerError
with open("crop_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
district_map = {
    "Ranchi": 0,
    "Dhanbad": 1,
    "Hazaribagh": 2,
    "Bokaro": 3,
    "Pakur": 4,
    "Garhwa":5,
    "West Singhbhum":6,
    "Godda":7,
    "Khunti":8,
    "East Singhbhum":9,
    "Dumka":10,
    "Koderma":11,
    "Jamtara":12,
    "Giridih":13,
    "Palamu":14,
    "Simdega":15,
    "Lateha":16,
    "Sahebganj":17,
    "Lohardaga":18,
    "Saraikela Kharsawan":19,
    "Ramgarh":20,
    "Chatra":21,
    "Latehar":22,
    "Deoghar":23
    
}

soil_map = {
    "Loamy": 0,
    "Clay": 1,
    "Sandy": 2,
    "Red Lateritic":3,
    "Alluvial":4,
    "Black":5
}

season_map = {
    "Kharif": 0,
    "Rabi": 1,
    "Zaid": 2
}
def get_weather_data(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key=YOUR_WEATHER_API_KEY&q={city}&aqi=no"
        res = requests.get(url, timeout=5).json()

        return (
            res["current"]["temp_c"],
            res["current"]["precip_mm"],
            res["current"]["humidity"],
            res["current"]["wind_kph"],
            18  
        )

    except:
        return 25, 0, 60, 5, 18
def get_soil_data():
    return {
        "N": random.randint(50, 150),              
        "P": random.randint(20, 80),
        "K": random.randint(20, 120),
        "pH": round(random.uniform(5.5, 7.5), 1),
        "OC": round(random.uniform(0.3, 1.2), 2),
        "EC": round(random.uniform(0.2, 1.5), 2),
        "Zn": round(random.uniform(0.5, 3.0), 2),
        "Fe": round(random.uniform(2.0, 10.0), 2),
        "Cu": round(random.uniform(0.2, 2.0), 2),
        "Mn": round(random.uniform(1.0, 6.0), 2),
        "Soil_Moisture": random.randint(20, 60)   
    }

def get_water_data():
     return {
        "Water_pH": round(random.uniform(6.5, 8.5), 1),
        "Water_EC": round(random.uniform(0.3, 2.5), 2),
        "TDS": random.randint(200, 1500),           # mg/L
        "Salinity": round(random.uniform(0.1, 1.5), 2),
        "Hardness": random.randint(80, 350)         # mg/L
    }

def get_agri_recommendation(crop, soil, water, weather, season):
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    Return ONLY valid JSON.

    Crop: {crop}
    Season: {season}
    Soil: {soil}
    Water: {water}
    Weather: {weather}

    {{
        "fertilizer": "...",
        "pesticide": "...",
        "irrigation": "..."
    }}
    """

    for _ in range(3):
        try:
            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return res.text
        except ServerError:
            time.sleep(2)

    return json.dumps({
        "fertilizer": "Balanced NPK as per crop stage",
        "pesticide": "Use pesticide only after pest scouting",
        "irrigation": "Irrigate based on soil moisture"
    })
def predict_crop(district, soil_type, season):
    d = district_map[district]
    s = soil_map[soil_type]
    se = season_map[season]

    temp, rain, hum, wind, solar = get_weather_data(district)
    soil = get_soil_data()
    water = get_water_data()

    X = np.array([[
        d,
        soil["N"], soil["P"], soil["K"],
        soil["pH"], soil["OC"], soil["EC"],
        soil["Zn"], soil["Fe"], soil["Cu"], soil["Mn"],
        soil["Soil_Moisture"],
        water["Water_pH"], water["Water_EC"], water["TDS"],
        water["Salinity"], water["Hardness"],
        temp, rain, hum, wind, solar,
        s,
        se
    ]])

    X_scaled = scaler.transform(X)
    crop = model.predict(X_scaled)

    weather = {
        "Temperature": temp,
        "Rainfall": rain,
        "Humidity": hum,
        "Wind_Speed": wind,
        "Solar_Radiation": solar
    }

    rec = get_agri_recommendation(crop, soil, water, weather, season)
    return crop, rec
st.set_page_config(page_title="AI Crop Recommendation", page_icon="🌾")
st.title(" AI-Based Crop Prediction System")

district = st.selectbox("District", district_map.keys())
soil_type = st.selectbox("Soil Type", soil_map.keys())
season = st.selectbox("Season", season_map.keys())

if st.button("Predict Crop & Recommendation"):
    with st.spinner("Predicting..."):
        crop, rec = predict_crop(district, soil_type, season)

    st.success(f" Predicted Crop: **{crop}**")

    try:
        st.json(json.loads(rec))
    except:
        st.text(rec)


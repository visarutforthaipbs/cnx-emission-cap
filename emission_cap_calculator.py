#!/usr/bin/env python3
"""
ระบบคำนวณค่ามลพิษอากาศเชียงใหม่-ลำพูน
โดยใช้แบบจำลองกล่องสมดุล (Steady-State Box Model)

สคริปต์นี้คำนวณค่ามลพิษรายวัน (ตัน/วัน) โดยพิจารณาจาก:
- ความเข้มข้น PM2.5 เป้าหมาย (37.5 ไมโครกรัม/ลูกบาศก์เมตร)
- สภาวะบรรยากาศแบบเรียลไทม์จาก Open-Meteo API
- ค่าคงที่ทางภูมิศาสตร์ของแอ่ง

สูตร: Q = (C × V) / τ
โดยที่:
  Q = ค่ามลพิษที่กำหนด
  C = ความเข้มข้นเป้าหมาย
  V = ปริมาตรอากาศในแอ่ง
  τ = เวลาหมุนเวียน
"""

import requests
from datetime import datetime
import json
import os


class EmissionCapCalculator:
    """คำนวณค่ามลพิษโดยใช้แบบจำลองกล่องสมดุล"""
    
    # ค่าคงที่
    TARGET_CONCENTRATION = 37.5  # µg/m³ (เป้าหมาย PM2.5)
    BASIN_AREA_KM2 = 1500  # km² (แอ่งเชียงใหม่-ลำพูน)
    BASIN_AREA_M2 = BASIN_AREA_KM2 * 1_000_000  # แปลงเป็น m²
    BASIN_LENGTH_KM = 80  # km (ความยาวเหนือ-ใต้)
    BASIN_LENGTH_M = BASIN_LENGTH_KM * 1000  # แปลงเป็น m
    
    # ตัวแปลงหน่วย
    KMH_TO_MS = 0.2778  # km/h เป็น m/s
    UG_PER_SEC_TO_TONS_PER_DAY = 8.64e-8  # µg/s เป็น Tons/Day
    
    # การตั้งค่า API
    LATITUDE = 18.7883  # พิกัดเชียงใหม่
    LONGITUDE = 98.9853
    API_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        """เริ่มต้นตัวคำนวณ"""
        self.blh_avg = None
        self.wind_speed_avg = None
        self.volume = None
        self.residence_time = None
        self.emission_cap_ug_s = None
        self.emission_cap_tons_day = None
    
    def fetch_weather_data(self):
        """ดึงข้อมูลความสูงชั้นผสมและความเร็วลมจาก Open-Meteo API"""
        params = {
            'latitude': self.LATITUDE,
            'longitude': self.LONGITUDE,
            'hourly': 'boundary_layer_height,wind_speed_10m',
            'forecast_days': 1,
            'timezone': 'Asia/Bangkok'
        }
        
        try:
            response = requests.get(self.API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # ดึงข้อมูลรายชั่วโมง (24 ชั่วโมง)
            hourly = data['hourly']
            blh_values = hourly['boundary_layer_height']  # หน่วยเป็นเมตร
            wind_speed_values = hourly['wind_speed_10m']  # หน่วยเป็น km/h
            
            # คำนวณค่าเฉลี่ย 24 ชั่วโมง
            # กรองค่า None ออก
            blh_filtered = [v for v in blh_values if v is not None]
            wind_filtered = [v for v in wind_speed_values if v is not None]
            
            if not blh_filtered or not wind_filtered:
                raise ValueError("ไม่มีข้อมูลที่ถูกต้องจาก API")
            
            self.blh_avg = sum(blh_filtered) / len(blh_filtered)
            self.wind_speed_avg = sum(wind_filtered) / len(wind_filtered)
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"เกิดข้อผิดพลาดในการดึงข้อมูลสภาพอากาศ: {e}")
            return False
        except (KeyError, ValueError) as e:
            print(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล API: {e}")
            return False
    
    def calculate_volume(self):
        """คำนวณปริมาตรอากาศในแอ่ง (V = พื้นที่ × ความสูง)"""
        self.volume = self.BASIN_AREA_M2 * self.blh_avg
        return self.volume
    
    def calculate_residence_time(self):
        """คำนวณเวลาหมุนเวียน (τ = ความยาว / ความเร็วลม)"""
        # แปลงความเร็วลมจาก km/h เป็น m/s
        wind_speed_ms = self.wind_speed_avg * self.KMH_TO_MS
        
        # คำนวณเวลาหมุนเวียนเป็นวินาที
        self.residence_time = self.BASIN_LENGTH_M / wind_speed_ms
        return self.residence_time
    
    def calculate_emission_cap(self):
        """คำนวณค่ามลพิษโดยใช้สูตรแบบจำลองกล่อง"""
        # Q = (C × V) / τ  (หน่วย µg/s)
        self.emission_cap_ug_s = (
            self.TARGET_CONCENTRATION * self.volume
        ) / self.residence_time
        
        # แปลงเป็น ตัน/วัน
        self.emission_cap_tons_day = (
            self.emission_cap_ug_s * self.UG_PER_SEC_TO_TONS_PER_DAY
        )
        
        return self.emission_cap_tons_day
    
    def print_results(self):
        """แสดงผลการคำนวณอย่างละเอียด"""
        print("\n" + "="*70)
        print("ระบบคำนวณค่ามลพิษเชียงใหม่-ลำพูน")
        print("แบบจำลองกล่องสมดุล (Steady-State Box Model)")
        print("="*70)
        
        print(f"\n📅 วันที่: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        print("\n📊 ค่าคงที่:")
        print(f"  ความเข้มข้นเป้าหมาย (C): {self.TARGET_CONCENTRATION} µg/m³")
        print(f"  พื้นที่แอ่ง: {self.BASIN_AREA_KM2:,.0f} ตร.กม. ({self.BASIN_AREA_M2:,.0f} ตร.ม.)")
        print(f"  ความยาวแอ่ง: {self.BASIN_LENGTH_KM} กม. ({self.BASIN_LENGTH_M:,} ม.)")
        
        print("\n🌤️  สภาวะบรรยากาศ (ค่าเฉลี่ย 24 ชั่วโมง):")
        print(f"  ความสูงชั้นผสม (BLH): {self.blh_avg:.1f} ม.")
        print(f"  ความเร็วลม: {self.wind_speed_avg:.2f} กม./ชม. ({self.wind_speed_avg * self.KMH_TO_MS:.2f} ม./วิ)")
        
        print("\n🔬 ค่าที่คำนวณได้:")
        print(f"  ปริมาตร (V): {self.volume:.2e} ลบ.ม.")
        print(f"  เวลาหมุนเวียน (τ): {self.residence_time:,.0f} วินาที ({self.residence_time/3600:.1f} ชั่วโมง)")
        print(f"  ค่ามลพิษ (Q): {self.emission_cap_ug_s:,.0f} µg/s")
        
        print("\n🎯 ผลลัพธ์สุดท้าย:")
        print(f"  ค่ามลพิษรายวัน: {self.emission_cap_tons_day:.2f} ตัน/วัน")
        print("="*70 + "\n")
    
    def save_results_json(self, filename='emission_cap_result.json'):
        """บันทึกผลลัพธ์ลงไฟล์ JSON"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'constants': {
                'target_concentration_ug_m3': self.TARGET_CONCENTRATION,
                'basin_area_km2': self.BASIN_AREA_KM2,
                'basin_length_km': self.BASIN_LENGTH_KM
            },
            'atmospheric_conditions': {
                'blh_avg_m': round(self.blh_avg, 1),
                'wind_speed_avg_kmh': round(self.wind_speed_avg, 2),
                'wind_speed_avg_ms': round(self.wind_speed_avg * self.KMH_TO_MS, 2)
            },
            'calculated_values': {
                'volume_m3': self.volume,
                'residence_time_seconds': round(self.residence_time, 0),
                'residence_time_hours': round(self.residence_time / 3600, 1),
                'emission_cap_ug_s': round(self.emission_cap_ug_s, 0)
            },
            'result': {
                'emission_cap_tons_day': round(self.emission_cap_tons_day, 2)
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ บันทึกผลลัพธ์ไปยัง {filename}")
    
    def save_to_historical_data(self, filename='data/historical_data.json'):
        """เพิ่มผลลัพธ์ปัจจุบันลงในไฟล์ข้อมูลประวัติ"""
        # สร้างโฟลเดอร์ data ถ้ายังไม่มี
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # โหลดข้อมูลประวัติที่มีอยู่
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    historical_data = json.load(f)
                except json.JSONDecodeError:
                    historical_data = []
        else:
            historical_data = []
        
        # สร้างรายการใหม่พร้อมข้อมูลแบบย่อสำหรับสร้างกราฟ
        new_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat(),
            'emission_cap_tons_day': round(self.emission_cap_tons_day, 2),
            'blh_avg_m': round(self.blh_avg, 1),
            'wind_speed_avg_kmh': round(self.wind_speed_avg, 2),
            'residence_time_hours': round(self.residence_time / 3600, 1)
        }
        
        # ตรวจสอบว่ามีรายการของวันนี้แล้วหรือยัง (อัปเดตแทนการเพิ่มใหม่)
        today = datetime.now().strftime('%Y-%m-%d')
        existing_index = None
        for i, entry in enumerate(historical_data):
            if entry.get('date') == today:
                existing_index = i
                break
        
        if existing_index is not None:
            historical_data[existing_index] = new_entry
            print(f"📝 อัปเดตรายการที่มีอยู่สำหรับวันที่ {today}")
        else:
            historical_data.append(new_entry)
            print(f"📝 เพิ่มรายการใหม่สำหรับวันที่ {today}")
        
        # บันทึกข้อมูลประวัติที่อัปเดตแล้ว
        with open(filename, 'w') as f:
            json.dump(historical_data, f, indent=2)
        
        print(f"✅ บันทึกข้อมูลประวัติไปยัง {filename}")

    
    def run(self):
        """ดำเนินการคำนวณทั้งหมด"""
        print("เริ่มการคำนวณค่ามลพิษ...")
        
        # ขั้นตอนที่ 1: ดึงข้อมูลสภาพอากาศ
        print("📡 กำลังดึงข้อมูลบรรยากาศจาก Open-Meteo API...")
        if not self.fetch_weather_data():
            print("❌ ไม่สามารถดึงข้อมูลสภาพอากาศได้ ออกจากโปรแกรม")
            return False
        
        print("✅ ดึงข้อมูลสภาพอากาศสำเร็จ")
        
        # ขั้นตอนที่ 2: คำนวณปริมาตร
        print("📦 กำลังคำนวณปริมาตรอากาศในแอ่ง...")
        self.calculate_volume()
        
        # ขั้นตอนที่ 3: คำนวณเวลาหมุนเวียน
        print("⏱️  กำลังคำนวณเวลาหมุนเวียน...")
        self.calculate_residence_time()
        
        # ขั้นตอนที่ 4: คำนวณค่ามลพิษ
        print("🎯 กำลังคำนวณค่ามลพิษ...")
        self.calculate_emission_cap()
        
        # ขั้นตอนที่ 5: แสดงผลลัพธ์
        self.print_results()
        
        # ขั้นตอนที่ 6: บันทึกเป็น JSON
        self.save_results_json()
        
        # ขั้นตอนที่ 7: บันทึกข้อมูลประวัติ
        self.save_to_historical_data()
        
        return True


def main():
    """จุดเริ่มต้นของโปรแกรม"""
    calculator = EmissionCapCalculator()
    calculator.run()


if __name__ == "__main__":
    main()

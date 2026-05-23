"""data_generator.py - Retail demand & cost generator | UT Austin OR Coursework"""
import numpy as np, pandas as pd

np.random.seed(42)
N_DCS, N_STORES, N_WEEKS = 3, 20, 52
DC_NAMES = ["DC_Midwest","DC_East","DC_West"]
STORE_NAMES = [f"Store_{i+1:02d}" for i in range(N_STORES)]
dc_capacity = np.array([9000,7500,8200])
store_zone  = np.array([1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,3,3])
base_demand = np.array([320,410,290,380,450,310,520,480,390,440,350,510,470,300,420,360,490,340,400,380])
weeks    = np.arange(N_WEEKS)
seasonal = (1.0+0.25*np.sin(2*np.pi*(weeks-10)/52))*np.where((weeks>=46)|(weeks<=2),1.45,1.0)
demand_matrix = np.maximum(np.outer(base_demand,seasonal)*np.random.normal(1.0,0.08,(N_STORES,N_WEEKS)),0).round().astype(int)
transport_cost = np.zeros((N_DCS,N_STORES))
for j,zone in enumerate(store_zone):
    for i in range(N_DCS):
        transport_cost[i,j]=np.random.uniform(*[(0.40,0.90),(1.10,1.80),(2.20,3.50)][min(abs(i+1-zone),2)])
transport_cost=transport_cost.round(2)
HOLDING_COST_PER_UNIT,SHORTAGE_PENALTY=0.18,6.50

def save_data(out_dir="data"):
    import os; os.makedirs(out_dir,exist_ok=True)
    avg=demand_matrix.mean(axis=1).round(1)
    pd.DataFrame({"store":STORE_NAMES,"zone":store_zone,"avg_weekly_demand":avg,"peak_weekly_demand":demand_matrix.max(axis=1)}).to_csv(f"{out_dir}/demand_data.csv",index=False)
    df=pd.DataFrame(transport_cost,index=DC_NAMES,columns=STORE_NAMES); df.index.name="dc"; df.to_csv(f"{out_dir}/transport_cost_matrix.csv")
    pd.DataFrame({"dc":DC_NAMES,"weekly_capacity":dc_capacity}).to_csv(f"{out_dir}/dc_supply.csv",index=False)
    print(f"Saved to {out_dir}/ | avg demand={avg.sum():.0f} | capacity={dc_capacity.sum()}")

if __name__=="__main__":
    save_data("data")

#%%
from spacepy import pycdf 
import pandas as pd
#%%
def read_shock_cdf(sn, path):

	cdf = pycdf.CDF(path)

	shock = cdf['SHOCK']

	output = []
	for i in range(len(shock)):

		if (sn - 1) * 27 <= i <= (sn - 1) * 27 + 26:
			output.append(shock[i])
	return output


def extract_values(line):
    return [float(value) if value.replace('.', '', 1).replace('-', '', 1).isdigit() else value for value in line.split()]

def parse_out_shocks(data):

	result = {
		"header": {"date": {}},
		"position": {},
		"time_windows": {},
		"Solar wind plasma and IMF": {"upstream": {}, "downstream": {}},
		"computed_parameters": {},
		"min_smr_index": None,
		"nx_ny_nz_values": []
	}
	result["header"]["sn"], result["header"]["date"]["year"], result["header"]["date"]["month"], result["header"]["date"]["day"], result["header"]["UTS"], result["header"]["UTM"] = extract_values(data[2])
	position_data = data[4].split('; ')
	result["position"] = {item.split(' = ')[0].strip(): float(item.split(' = ')[1].replace(' Re', '')) for item in position_data}
	result["time_windows"]["upstream"] = data[7].split(': ')[1].strip()
	result["time_windows"]["downstream"] = data[8].split(': ')[1].strip()

	solar_wind_labels = data[11].split()
	solar_wind_upstream = extract_values(data[12])
	solar_wind_downstream = extract_values(data[13])

	result["Solar wind plasma and IMF"]["upstream"] = dict(zip(solar_wind_labels, solar_wind_upstream[1:]))
	result["Solar wind plasma and IMF"]["downstream"] = dict(zip(solar_wind_labels, solar_wind_downstream[1:]))

	computed_params_labels = data[16].split()
	computed_params_values = extract_values(data[17])
	result["computed_parameters"] = dict(zip(computed_params_labels, computed_params_values))

	result["min_smr_index"] = float(data[19].split(': ')[1].strip().replace(' nT', ''))

	shock_paramns_labels = data[21].split()
	calc_methods = []
	nx_ny_nz_values = []
	for i in range(22, 27):
		nx_ny_nz_values.append(extract_values(data[i])[1:])
		calc_methods.append(extract_values(data[i])[0])
	result["nx_ny_nz_values"] = pd.DataFrame(nx_ny_nz_values, index = calc_methods, columns=shock_paramns_labels)


	return result
# %%
PATH_SHOCKS = '/Users/jose/mag_data/shocks/full_shock_params.cdf'
data = read_shock_cdf(143, path = PATH_SHOCKS)
# %%
result = parse_out_shocks(data)
# %%

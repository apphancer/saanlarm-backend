import random
import time
import json
import subprocess

def generate_cycles(leds, colour, min_value, max_value, total_values, num_values_per_cycle, step_time):
    available_numbers = list(range(min_value, max_value + 1))
    random.shuffle(available_numbers)
    cycles = []

    for i in range(int(total_values / num_values_per_cycle)):
        pair = available_numbers[:num_values_per_cycle]
        available_numbers = available_numbers[num_values_per_cycle:]

        for pixel in pair:
            if colour not in leds[pixel]:
                leds[pixel][colour] = 0
            leds[pixel][colour] += 1

        cycles.extend(pair)

        leds_dict = {idx: led for idx, led in enumerate(leds)}


        updated_leds = {}
        for idx, led in leds_dict.items():
            if any(led.values()):
                if idx not in updated_leds:
                    updated_leds[idx] = {}
                updated_leds[idx].update(led)

        print(f"Cycle {colour} {i}: {json.dumps(updated_leds, sort_keys=True)}")

        json_data = json.dumps(updated_leds)
        subprocess.run(['python', 'php-reader.py'], input=json_data, text=True, check=True)

        time.sleep(step_time)

    print("--------")



min_value = 1
max_value = 150
num_values_per_cycle = 10
total_values = max_value - min_value + 1

leds = [{} for _ in range(max_value + 1)]

cycles = 12 # @todo: calculate this from number of calls to generate_cycles
steps_per_cycle = total_values / num_values_per_cycle
total_steps = steps_per_cycle * cycles
total_minutes = 0.25 # // @todo[m]: something is wrong with this
step_time = (total_minutes * 60) / total_steps
print(f"Total Cycles: {cycles} | Total Steps Per Cycle: {steps_per_cycle} | Total Steps: {total_steps} | Step Time: {step_time} s")


generate_cycles(leds, 'R', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)
generate_cycles(leds, 'W', min_value, max_value, total_values, num_values_per_cycle, step_time)

# Sort 'leds' within the 'generate_cycles' function and for final output
leds.sort(key=lambda x: next((k for k in x.keys() if isinstance(k, int)), -1))
filtered_leds_final = [led for led in leds if led]
print(json.dumps(filtered_leds_final, sort_keys=True))

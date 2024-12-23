import random
import time
import json
import subprocess
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config_local as config

num_pixels = config.NUM_PIXELS

min_leds = 1
max_leds = num_pixels
num_leds_per_cycle = 15 # move to config




red_brightness = 2  # move to config
white_brightness = 5  # move to config
cycles1 = red_brightness + white_brightness
total_minutes1 = 1.5 # move to config 1.5



cycles2 = 50 # move to config 25
total_minutes2 = 1.5 # move to config 1.5


cycle3 = 255
total_minutes3 = 1.5 # move to config 1.5


process = subprocess.Popen(['python', 'ledWriter.py'], stdin=subprocess.PIPE, text=True)

def send_led_command(data):
    process.stdin.write(data + "\n")
    process.stdin.flush()

def generate_cycles(leds, colour, min_leds, max_leds, total_leds, num_leds_per_cycle, step_time):
    available_numbers = list(range(min_leds, max_leds + 1))
    random.shuffle(available_numbers)
    cycles = []

    for i in range(int(total_leds / num_leds_per_cycle)):
        pair = available_numbers[:num_leds_per_cycle]
        available_numbers = available_numbers[num_leds_per_cycle:]

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

        # print(f"Cycle {colour} {i}: {json.dumps(updated_leds, sort_keys=True)}")
        print(f"LED Cycle {i}: {colour} = {leds[pixel][colour]}")


        json_data = json.dumps(updated_leds)

        send_led_command(json_data)

        time.sleep(step_time)

    print("--------")


total_leds = max_leds - min_leds + 1
leds = [{} for _ in range(max_leds + 1)]
steps_per_cycle = total_leds / num_leds_per_cycle





total_steps = steps_per_cycle * cycles1
step_time = (total_minutes1 * 60) / total_steps

print(f"-------")
print(f"-------")
print(f"STAGE 1 | Total Cycles: {cycles1} | Total Steps Per Cycle: {steps_per_cycle} | Total Steps: {total_steps} | Step Time: {step_time} s")
print(f"-------")
print(f"-------")

cycles_config = [('R', red_brightness)] + [('W', white_brightness)]

for colour, count in cycles_config:
    for _ in range(count):
        print(f"Cycle {_}")
        print(f"-------")
        generate_cycles(leds, colour, min_leds, max_leds, total_leds, num_leds_per_cycle, step_time)



total_steps = steps_per_cycle * cycles2
step_time = (total_minutes2 * 60) / total_steps
print(f"-------")
print(f"-------")
print(f"STAGE 2 | Total Cycles: {cycles2} | Total Steps Per Cycle: {steps_per_cycle} | Total Steps: {total_steps} | Step Time: {step_time} s")
print(f"-------")
print(f"-------")

for _ in range(cycles2):
    print(f"Cycle {_}")
    print(f"-------")
    generate_cycles(leds, 'W', min_leds, max_leds, total_leds, num_leds_per_cycle, step_time)


# leds.sort(key=lambda x: next((k for k in x.keys() if isinstance(k, int)), -1))
# filtered_leds_final = [led for led in leds if led]
# print(json.dumps(filtered_leds_final, sort_keys=True))


total_steps = cycle3 - (white_brightness+cycles2)
step_time = (total_minutes3 * 60) / total_steps

print(f"-------")
print(f"-------")
print(f"Stage 3 | Update LEDs incrementally to max value | Total Steps: {total_steps} | Step Time: {step_time} s")
print(f"-------")
print(f"-------")


current_brightness = (white_brightness+cycles2)

for iteration in range(total_steps):
    current_brightness += 1
    updated_leds = {idx: {'W': current_brightness} for idx in range(min_leds, max_leds + 1)}

    #print(f"Cycle {iteration + 1}/{total_steps}: {json.dumps(updated_leds, sort_keys=True)}")
    print(f"LED Cycle {iteration}: W = {current_brightness}")

    json_data = json.dumps(updated_leds)
    send_led_command(json_data)

    time.sleep(step_time)
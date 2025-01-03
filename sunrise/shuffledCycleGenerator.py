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
num_leds_per_cycle = config.SUNRISE_NUM_LEDS_PER_CYCLE

phase1_red_max = config.SUNRISE_PHASE_1_RED_MAX_BRIGHTNESS
phase1_white_max = config.SUNRISE_PHASE_1_WHITE_MAX_BRIGHTNESS
phase1_cycles = phase1_red_max + phase1_white_max
phase1_total_minutes = config.SUNRISE_PHASE_1_TOTAL_MINUTES

phase2_cycles = config.SUNRISE_PHASE_2_WHITE_MAX_BRIGHTNESS
phase2_total_minutes = config.SUNRISE_PHASE_2_TOTAL_MINUTES

phase3_cycles = config.SUNRISE_PHASE_3_WHITE_MAX_BRIGHTNESS
phase3_total_minutes = config.SUNRISE_PHASE_3_TOTAL_MINUTES

script_dir = os.path.dirname(os.path.abspath(__file__))
led_writer_path = os.path.join(script_dir, "ledWriter.py")

# Start the LED writer process for sending LED commands
process = subprocess.Popen(['python', led_writer_path], stdin=subprocess.PIPE, text=True)


def send_led_command(data):
    """Send a JSON payload to the LED writer process."""
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




def start_sunrise_cycle(fade_in_event):
    """
    Start the sunrise LED cycle across three phases:
    Phase 1 - Warm-up with red and white LEDs
    Phase 2 - Bright white LEDs
    Phase 3 - Incrementally max out the brightness.
    """
    total_leds = max_leds - min_leds + 1
    leds = [{} for _ in range(max_leds + 1)]
    steps_per_cycle = total_leds / num_leds_per_cycle

    # Phase 1 - Warm-up with red and white LEDs
    total_steps = steps_per_cycle * phase1_cycles
    step_time = (phase1_total_minutes * 60) / total_steps
    print(f"STAGE 1 | Total Cycles: {phase1_cycles} | Total Steps Per Cycle: {steps_per_cycle} | Total Steps: {total_steps} | Step Time: {step_time} s")
    cycles_config = [('R', phase1_red_max)] + [('W', phase1_white_max)]

    for colour, count in cycles_config:
        for _ in range(count):
            if fade_in_event.is_set():  # Check if the process should continue
                generate_cycles(leds, colour, min_leds, max_leds, total_leds, num_leds_per_cycle, step_time)
            else:
                print("Sunrise interrupted during Phase 1")
                return

    # Phase 2 - Bright white LEDs
    total_steps = steps_per_cycle * phase2_cycles
    step_time = (phase2_total_minutes * 60) / total_steps
    print(f"STAGE 2 | Total Cycles: {phase2_cycles} | Total Steps Per Cycle: {steps_per_cycle} | Total Steps: {total_steps} | Step Time: {step_time} s")

    for _ in range(phase2_cycles):
        if fade_in_event.is_set():
            generate_cycles(leds, 'W', min_leds, max_leds, total_leds, num_leds_per_cycle, step_time)
        else:
            print("Sunrise interrupted during Phase 2")
            return

    # Phase 3 - Incrementally max out brightness
    total_steps = phase3_cycles - (phase1_white_max + phase2_cycles)
    step_time = (phase3_total_minutes * 60) / total_steps
    print(f"Stage 3 | Update LEDs incrementally to max value | Total Steps: {total_steps} | Step Time: {step_time} s")
    current_brightness = phase1_white_max + phase2_cycles

    for iteration in range(total_steps):
        if fade_in_event.is_set():
            current_brightness += 1
            updated_leds = {
                idx: {'W': current_brightness}
                for idx in range(min_leds, max_leds + 1)
            }

            print(f"LED Cycle {iteration}: W = {current_brightness}")
            json_data = json.dumps(updated_leds)
            send_led_command(json_data)

            time.sleep(step_time)
        else:
            print("Sunrise interrupted during Phase 3")
            return
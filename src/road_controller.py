from Slot import Slot
import car_controller as cc
from constants import *


# --- Link related functions ---

def insert_links(Vissim):
    wkt_linestring_vertical = "LINESTRING (0 -100, 0 100)"
    wkt_linestring_horizontal = "LINESTRING (-100 0, 100 0)"
    lane_width = [3.5]
    
    Vissim.Net.Links.AddLink(1, wkt_linestring_vertical, lane_width)
    Vissim.Net.Links.AddLink(2, wkt_linestring_horizontal, lane_width)

# --- Link related functions --- End


# --- Slot related functions ---

def try_add_new_slot(slots_list, link, lane, speed, accept_vehicle, offset=0):
    if len(slots_list) == 0:
        new_slot = Slot(link, lane, speed, None, accept_vehicle, offset=offset)
        slots_list.append(new_slot)
    else:
        last_slot = slots_list[-1]
        if last_slot.position >= -1:
            offset = last_slot.position - (last_slot.length/2)
            new_slot_accept_vehicle = not last_slot.accepts_vehicle
            new_slot = Slot(link, lane, speed, None, new_slot_accept_vehicle, offset)
            slots_list.append(new_slot)
        # else:   # Do nothing


def step_forward_all_slots(slots_array_1, slots_array_2, sim_delta_time):
    for slot in slots_array_1:
        slot.step_forward(sim_delta_time)
    
    for slot in slots_array_2:
        slot.step_forward(sim_delta_time)


# get slot in conflict area of specific lane of specific link
def get_slots_in_conflict_area(slots):
    slots_in_conflict_area = []
    for slot in slots:
        if slot.get_front_border_position() > CONFLICT_AREA_START_HORIZONTAL and slot.get_back_border_position() < CONFLICT_AREA_END_HORIZONTAL:
            slots_in_conflict_area.append(slot)

    return slots_in_conflict_area


def remove_slot_after_end_of_road(slots_list):
    for slot in slots_list:
        if slot.position > LINK_LENGTH + slot.length:
            slots_list.remove(slot)


# only one slot of type "accepts_vehicle" may be in conflicting area
def is_conflict_area_slots_safe(slots_horizontal, slots_vertical):
    slots_conflict_area_horizontal = get_slots_in_conflict_area(slots_horizontal)
    slots_conflict_area_vertical = get_slots_in_conflict_area(slots_vertical)
    
    # if any link is empty, there is no conflict, it is safe
    if slots_conflict_area_horizontal == [] or slots_conflict_area_vertical == []:
        return True
    
    # else, check if any combination of slots currently in the conflict area accept vehicles
    for slot_h in slots_conflict_area_horizontal:
        for slot_v in slots_conflict_area_vertical:
            if slot_h.accepts_vehicle and slot_v.accepts_vehicle:   # if both slots may contain a vehicle, the area is not safe
                return False
    return True

# --- Slot related functions --- End


# --- Vehicle related functions ---

def check_collisions(all_vehicles_in_simulation):
    for vehicle_reference in all_vehicles_in_simulation:
        if cc.is_vehicle_in_confilct_area(vehicle_reference):
            for vehicle in all_vehicles_in_simulation:
                if vehicle_reference.AttValue('No') != vehicle.AttValue('No'):
                    if abs(vehicle_reference.AttValue('Pos') - vehicle.AttValue('Pos')) < vehicle.AttValue('Length')/2 or abs(vehicle_reference.AttValue('Pos') - vehicle.AttValue('Pos')) < vehicle_reference.AttValue('Length')/2:
                        print("collision", vehicle_reference.AttValue('No'), vehicle_reference.AttValue('Lane'), vehicle_reference.AttValue('Pos'), vehicle.AttValue('No'), vehicle.AttValue('Lane'), vehicle.AttValue('Pos'))

# --- Vehicle related functions --- End

from constants import *


# --- Link related functions ---

def insert_vehicle_to_link(Vissim, desired_speed, link, lane, xcoordinate):
    vehicle_type = 100
    # xcoordinate = 0 # unit according to the user setting in Vissim [m or ft]
    interaction = False # optional boolean
    vehicle_inserted = Vissim.Net.Vehicles.AddVehicleAtLinkPosition(vehicle_type, link, lane, xcoordinate, desired_speed, interaction)
    vehicle_inserted.SetAttValue('Speed', desired_speed)
    vehicle_inserted.SetAttValue('DesSpeed', desired_speed)
    return vehicle_inserted


def get_vehicle_link(vehicle):
    veh_linklane = vehicle.AttValue('Lane') # format: 2-1   (link: 2, lane: 1)
    return int(veh_linklane.split("-")[0])


def is_vehicle_in_confilct_area(vehicle):
    vehicle_position = vehicle.AttValue('Pos')
    if vehicle_position >= (LINK_LENGTH - LINK_WIDTH)/2 and vehicle_position <= (LINK_LENGTH + LINK_WIDTH)/2:
        return True
    else:
        return False
    

# check if there is an available slot for car to enter link and lane
def can_car_enter_link_lane(slots_link):
    for slot in slots_link:     # looks for the slot which is over the start of the lane
        if slot.get_back_border_position() < 0 < slot.get_front_border_position():
            if slot.accepts_vehicle and slot.vehicle == None:   # if it accepts vehicles and doesn't have one
                return slot                                     # returns slot
    
    return False    # if there is no slot in this condition, return False

# --- Link related functions --- End


# --- Slot related functions ---
def get_distance_vehicle_from_slot_center(slot_list):
    for slot in slot_list:
        if slot.vehicle:
            vehicle = slot.vehicle
            print(vehicle.AttValue('Speed'), vehicle.AttValue('Pos') - slot.position, vehicle.AttValue('Pos'), slot.position)
            return vehicle.AttValue('Pos') - slot.position


def is_vehicle_within_slot_limits(slot):
    # if slot does not accept vehicle or have no vehicle assigned, return None
    if slot.vehicle is None:
        return None
    
    # else, calculate positions (front and back) and check if vehicle is within slot
    veh_length = slot.vehicle.AttValue('Length')
    veh_position = slot.vehicle.AttValue('Pos')
    veh_front_limit = veh_position + (veh_length/2)
    veh_back_limit = veh_position - (veh_length/2)
    
    slot_front_limit = slot.get_front_border_position()
    slot_back_limit = slot.get_back_border_position()

    if slot_front_limit - veh_front_limit < 0 or veh_back_limit - slot_back_limit < 0:
        return False
    else:
        return True

# --- Slot related functions --- End

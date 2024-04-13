import win32com.client as com
import sys
from Slot import Slot
import car_controller as cc
import road_controller as rc
from constants import *
from Logger import Logger


def setup_network():
    # Connecting the COM Server
    Vissim = com.Dispatch("Vissim.Vissim")
    Vissim.New()

    # Load Vissim network
    filename = "C:\\Projects\\Mestrado\\vissim\\hello_world\\hello.inpx"
    # flag_read_additionally = True # you can read network(elements) additionally, in this case set "flag_read_additionally" to true
    Vissim.LoadNet(filename) #, flag_read_additionally)

    ## Load a Layout:
    layout_addr = "C:\\Projects\\Mestrado\\vissim\\hello_world\\hello.layx"
    Vissim.LoadLayout(layout_addr)

    # Insert 2 perpendicular links
    new_link = rc.insert_links(Vissim)

    return Vissim


# Simulate vehicle starting at center of slot with same speed
def simulate_center_same_speed(Vissim):
    # Create logger
    logger = Logger()

    # Array of slots
    slots_link_1 = []
    slots_link_2 = []

    # Starting time
    sim_initial_time = 0
    for i in range(1000):
        Vissim.Simulation.RunSingleStep()
        sim_final_time = Vissim.Simulation.AttValue("SimSec")
        sim_delta_time = sim_final_time - sim_initial_time
        sim_initial_time = sim_final_time

        # check if conflict area state is safe
        is_conflict_area_safe = rc.is_conflict_area_slots_safe(slots_link_1, slots_link_2)
        if not is_conflict_area_safe:
            logger.write_log('Conflict area slot safety', is_conflict_area_safe)

        # move all slots one step forward
        rc.step_forward_all_slots(slots_link_1, slots_link_2, sim_delta_time)

        # insert new slots if it should
        rc.try_add_new_slot(slots_link_1, 1, 1, SLOT_SPEED, accept_vehicle=False, offset=-0.75)    # link 1
        rc.try_add_new_slot(slots_link_2, 2, 1, SLOT_SPEED, accept_vehicle=True, offset=-4.25)   # link 2

        # remove slots after end of road
        rc.remove_slot_after_end_of_road(slots_link_1)
        rc.remove_slot_after_end_of_road(slots_link_2)

        # check if links could receive a car
        can_link_1_1_receive_car = cc.can_car_enter_link_lane(slots_link_1)
        can_link_2_1_receive_car = cc.can_car_enter_link_lane(slots_link_2)

        # if each link can receive a car, insert a car
        if can_link_1_1_receive_car:
            slot_1 = can_link_1_1_receive_car
            start_position = can_link_1_1_receive_car.position
            veh_1 = cc.insert_vehicle_to_link(Vissim, VEHICLE_SPEED, 1, 1, start_position)
            slot_1.vehicle = veh_1
        if can_link_2_1_receive_car:
            slot_2 = can_link_2_1_receive_car
            start_position = can_link_2_1_receive_car.position
            veh_2 = cc.insert_vehicle_to_link(Vissim, VEHICLE_SPEED, 2, 1, start_position)
            slot_2.vehicle = veh_2

        # every iteration, check if any vehicle is out of slot limits, if it is, write log
        for slot in slots_link_1:
            if cc.is_vehicle_within_slot_limits(slot) is False:
                if slot.vehicle.AttValue('Pos') < 60:
                    logger.write_log('vehicle_out_of_slot_limits_on_link_1 (id, speed, pos)', slot.vehicle.AttValue('No'), slot.vehicle.AttValue('Speed'), slot.vehicle.AttValue('Pos'))
        for slot in slots_link_2:
            if cc.is_vehicle_within_slot_limits(slot) is False:
                if slot.vehicle.AttValue('Pos') < 60:
                    logger.write_log('vehicle_out_of_slot_limits_on_link_2 (id, speed, pos)', slot.vehicle.AttValue('No'), slot.vehicle.AttValue('Speed'), slot.vehicle.AttValue('Pos'))
        
        # Every N iteractions, print 
        if i%20 == 0:
            all_vehicles = Vissim.Net.Vehicles.GetAll()
            print("Vehicles in simulation:", len(all_vehicles))
            # for cur_Veh in all_vehicles:
            #     veh_number      = cur_Veh.AttValue('No')
            #     veh_type        = cur_Veh.AttValue('VehType')
            #     veh_speed       = cur_Veh.AttValue('Speed')
            #     veh_position    = cur_Veh.AttValue('Pos')
            #     veh_linklane    = cur_Veh.AttValue('Lane')
            #     # veh_length      = cur_Veh.AttValue('Length')
            #     # veh_width       = cur_Veh.AttValue('Width')
            #     # print('%s  |  %s  |  %.2f  |  %.2f  |  %s  |  %.2f  |  %.2f' % (veh_number, veh_type, veh_speed, veh_position, veh_linklane, veh_length, veh_width))
            #     # print('%.2f' % (veh_position), veh_linklane, veh_length)
            #     veh_id_link_position = {"id": veh_number, "link": int(veh_linklane.split("-")[0]), "position": veh_position}

            #     print("veh_type:", veh_type)
            #     print("veh_speed:", veh_speed)
            #     print("---------------------------------------------")

    

if __name__ == "__main__":
    network = setup_network()
    simulation = simulate_center_same_speed(network)
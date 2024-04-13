class Slot:
    def __init__(self, link, lane, speed, vehicle, accepts_vehicle, offset = 0) -> None:
        self.accepts_vehicle = accepts_vehicle

        if accepts_vehicle:
            self.length = 7
        else:
            self.length = 14
            
        self.position =  offset - (self.length/2)   # position of the center of the slot
        self.link = link
        self.lane = lane
        self.speed = speed
        self.vehicle = vehicle
        
        
    def __str__(self) -> str:
        return f"lane: {self.lane}, position: {self.position}, speed: {self.speed}"
    

    def step_forward(self, delta_time):
        speed_mps = self.speed / 3.6        # convert speed from km/h to m/s
        self.position += speed_mps * delta_time    # update slot position
    
    
    def get_front_border_position(self):
        return self.position + (self.length/2)
    

    def get_back_border_position(self):
        return self.position - (self.length/2)
    
    
    def get_vehicle_position_in_slot(self):
        if self.vehicle is None:
            return None
        return self.position - self.vehicle.AttValue('Pos')

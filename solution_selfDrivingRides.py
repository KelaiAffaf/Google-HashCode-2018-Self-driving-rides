from __future__ import print_function

import math
import sys


def get_distance(ra, ca, rb, cb):
    return abs(ra-rb)+abs(ca-cb)

class Ride(object):

    def __init__(self, id,a, b, x, y , s, f ):
        self.id = id
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.s = s
        self.f = f

    def __eq__(self, other):
        return (self.s, -self.f) == (other.s , -other.f)

    def __le__(self, other):
        return (self.s, -self.f) <= (other.s , -other.f)

    def __ge__(self, other):
        return (self.s, -self.f) >= (other.s , -other.f)  

    def __gt__(self, other):
        return (self.s, -self.f) > (other.s , -other.f)

    def __ne__(self, other):
        return (self.s, -self.f) != (other.s , -other.f)

    def __lt__(self, other):
        return (self.s, -self.f) < (other.s , -other.f)

class Vehicle(object): 
    def __init__(self,id,actual_step, x, y):
        self.id = id
        self.x = x
        self.y = y 
        self.actual_step = actual_step 
        self.score = 0
        self.rides = []

    def get_position(self): 
        return (self.x, self.y)

    def get_total_steps(self, ride):
        total_steps = get_distance(self.x, self.y, ride.a, ride.b) + get_distance(ride.a, ride.b, ride.x, ride.y)
        return total_steps
    
    def has_bonus(self, ride): 
        steps_to_start = get_distance(self.x, self.y, ride.a, ride.b)
        if steps_to_start + self.actual_step <= ride.s :
            return True
        else:
            return False 

    def is_possible(self, ride, grid ):
        #steps_to_ride_end = self.get_total_steps(ride) + self.actual_step
        #steps_to_ride_start = get_distance(self.x, self.y, ride.a, ride.b) + self.actual_step
       
        satisfied_ride = self.get_total_steps(ride) + self.actual_step < ride.f
        
        return satisfied_ride 
    
    def get_ride_score(self, ride, grid ):
        if self.is_possible(ride, grid): 
            if self.has_bonus(ride):
                return grid.bonus + ride.f - (ride.s + get_distance(ride.a, ride.b, ride.x, ride.y)) 
            else : 
                return  (ride.f - self.get_total_steps(ride)+ self.actual_step)
        else: 
            return 0 
    
    def go_ride(self, ride): 
        if self.has_bonus(ride):
              self.actual_step += ride.s - (self.actual_step + get_distance(self.x, self.y, ride.a, ride.b))
        self.actual_step += self.get_total_steps(ride) 
        self.x = ride.x
        self.y = ride.y
        self.rides.append(ride.id)

    def __eq__(self, other):
        return self.actual_step == other.actual_step 

    def __le__(self, other):
        return self.actual_step <= other.actual_step

    def __ge__(self, other):
        return self.actual_step >= other.actual_step  

    def __gt__(self, other):
        return self.actual_step > other.actual_step

    def __ne__(self, other):
        return self.actual_step != other.actual_step

    def __lt__(self, other):
        return self.actual_step < other.actual_step

class Grid(object):

    def __init__(self, rows, cols,  num_vehicles, num_rides, bonus,num_steps,
                rides):
        self.rows = rows
        self.cols = cols
        self.grid = []
        for i in range(1, rows):
            self.grid.append([0] * cols)
        self.num_vehicles = num_vehicles
        self.num_rides = num_rides 
        self.vehicles = []
        for i in range(num_vehicles): 
            self.vehicles.append(Vehicle(i,0,0,0))
        self.bonus = bonus
        self.num_steps = num_steps
        self.rides = rides
        self.score = 0 # Actual scoring 


    def define_ride_vehicles(self):
        self.rides.sort()
        for r in self.rides: 
            self.vehicles.sort()
            max_score = 0 
            suitable_vehicule = None
            for v in self.vehicles:
                if v.actual_step <= r.s :
                    score = v.get_ride_score(r, self)
                    if score > max_score : 
                        max_score = score 
                        suitable_vehicule = v       
                else: 
                    break
            if max_score > 0 :
                suitable_vehicule.go_ride(r)

def read_file(filename):
    """Reading input file."""
    grid = None
    with open(filename, 'r') as fin:
        line = fin.readline() 
        rows, cols, num_vehicles, num_rides, bonus,num_steps = [
            int(num) for num in line.split()]

        rides = []
        for i in range(num_rides):
            line = fin.readline()
            a,b, x,y , s, f = [int(num) for num in line.split()]
            rides.append(Ride(i,a,b, x,y,s, f))

        rides.sort()
        grid = Grid(rows, cols, num_vehicles, num_rides, bonus,num_steps, rides)
    return grid


def write_file(grid, filename):
    """Write output file."""
    with open(filename, 'w') as fout:
        for v in  grid.vehicles:
            fout.write(" "+str(len(v.rides))+" "+ " ".join( ""+str(r)+"" for r in v.rides) + '\n')

def main():
    """Main function"""
    filename = "e_high_bonus.in"

    print('Running on file: %s' % filename )

    # read input file
    grid = read_file(filename)
    try:
        grid.define_ride_vehicles()
    except KeyboardInterrupt:
        pass

    #write output file
    write_file(grid,"out.in")
    print("finish")


if __name__ == '__main__':
    main()
/***
* Name: Individual
* Author: admin_ptaillandie
* Description: 
* Tags: Tag1, Tag2, TagN
***/
model SWITCH

import "Crossroad.gaml"
import "../../Constants.gaml"
import "../../Parameters.gaml"
import "../../logger.gaml"
import "../transport_species/Transport.gaml"
import "../transport_species/Bike.gaml"
import "../transport_species/Walk.gaml"
import "../transport_species/Bus.gaml"
import "../data_structure_species/SortedMap.gaml"
import "../data_structure_species/Queue.gaml"

species Road {

//type of road (the OpenStreetMap highway feature: https://wiki.openstreetmap.org/wiki/Map_Features)
	string type;
	string urban_context <- "urban" among: ["urban", "interurban", nil];

	//is roundabout or not (OSM information)
	string junction;

	//start crossroad node
	Crossroad start_node;

	//end crossroad node
	Crossroad end_node;
	
	point trans;

	//maximum legal speed on this road
	float max_speed;

	//average speed on this road
	float avg_speed <- road_speed.keys contains [type, urban_context, weather] ? road_speed[[type, urban_context, weather]] * road_speed_avg_coef[type] : 50.0;

	//number of motorized vehicule lane in this road
	int nb_lanes <- 1;

	//is the road is oneway or not
	string oneway;

	//foot=no means pedestrians are not allowed
	string foot;

	//bicycle=no means bikes are not allowed
	string bicycle;

	// access=no means car are not allowed
	string access;

	// access=no together with bus=yes means only buses are allowed 
	string bus;

	// tag is used to describe the "physical" properties of the road.
	string parking_lane;

	//is used to give information about footways
	string sidewalk;

	// can be used to describe any cycle lanes constructed within the carriageway or cycle tracks running parallel to the carriageway.
	string cycleway;

	//length of the road (in meters)
	float size <- shape.perimeter;

	// the minimal time between two vehicules leaving the road (in second)
	float output_flow_capacity <- output_flow.keys contains type ? output_flow[type] : 2.4;

	//maximum space capacity of the road (in meters)
	float max_capacity <- size * nb_lanes min: 15.0;

	//actual free space capacity of the road (in meters)
	float current_capacity <- max_capacity min: 0.0 max: max_capacity;
	
	bool is_jammed function: (occupation_ratio > jam_threshold) and (max_capacity > 25.0);
	
	float occupation_ratio function: (max_capacity - current_capacity) / max_capacity;
	
	//has_bike_lane = true if there is a specific lane for bikes in this road
	//				= false if not
	bool has_bike_lane <- false;
	bool has_bus_lane <- false;

	//lists of current vehicules present in the road 
	list<Walk> present_pedestrians <- [];
	list<Bike> present_bikes <- [];
	Queue present_transports <- [];
	Queue present_buses <- [];

	//This list store all the incoming transports requests by chronological order
	//waiting_transports = [[float time_request, Transport t]]
	SortedMap waiting_transports;

	init {
		size <- shape.perimeter;
		max_capacity <- size * nb_lanes;
		current_capacity <- max_capacity;
		create SortedMap {
			myself.waiting_transports <- self;
		}
		create Queue {
			myself.present_transports <- self;
		}
		create Queue {
			myself.present_buses <- self;
		}
	}

	action enterRequest (Transport t, float request_time) {
		switch species(t) {
			match Bike {
				if not has_bike_lane {
					current_capacity <- current_capacity - t.size;
				}

				ask t {
					do setEntryTime(request_time with_precision 3);
				}

			}

			match Walk {
				ask t {
					do setEntryTime(request_time with_precision 3);
				}

			}
			
			match Bus{
				if not has_bus_lane {
					if hasCapacity(t.size) {
						ask t {
							myself.current_capacity <- myself.current_capacity - t.size;
							do setEntryTime(request_time with_precision 3);
						}
					} else {
						ask waiting_transports {
							do add([request_time, t]);
						}
					}
				}else{
					ask t {
							myself.current_capacity <- myself.current_capacity - t.size;
							do setEntryTime(request_time with_precision 3);
					}
				}
			}

			default {
				if hasCapacity(t.size) {
					ask t {
						myself.current_capacity <- myself.current_capacity - t.size;
						do setEntryTime(request_time with_precision 3);
					}
				} else {
					ask waiting_transports {
						do add([request_time, t]);
					}

				}

			}

		}

	}

	action acceptTransport (float entry_time) {
		if not waiting_transports.isEmpty() {
			Transport t <- getWaitingTransport(0);
			float request_time <- getWaitingTimeRequest(0);
			int delay <- 0;
			loop while: hasCapacity(t.size) and not waiting_transports.isEmpty() {
				ask t {
					myself.current_capacity <- myself.current_capacity - t.size;
					do setEntryTime(entry_time with_precision 3);
				}
				ask waiting_transports {
					do remove(0);
				}

				if not waiting_transports.isEmpty() {
					t <- getWaitingTransport(0);
					request_time <- getWaitingTimeRequest(0);
				}

			}

		}

	}

	action queueInRoad (Transport t, float entry_time) {
		switch species(t) {
			match Bike {
				present_bikes << Bike(t);
				ask t {
					float leave_time <- entry_time + getRoadTravelTime(myself);
					do setLeaveTime(leave_time with_precision 3);
				}
			}

			match Walk {
				present_pedestrians << Walk(t);
				ask t {
					float leave_time <- entry_time + getRoadTravelTime(myself);
					do setLeaveTime(leave_time with_precision 3);
				}
			}
			
			match Bus {
				float leave_time;
				ask t {
					leave_time <- entry_time + getRoadTravelTime(myself);
				}
				if has_bus_lane{
					if present_buses.isEmpty() {
						ask t {
							do setLeaveTime(leave_time with_precision 3);
						}
					}
					ask present_buses {
						do add([leave_time, t]);
					}
				}else{
					if present_transports.isEmpty() {
						ask t {
							do setLeaveTime(leave_time with_precision 3);
						}
					}
					ask present_transports {
						do add([leave_time, t]);
					}
				}
			}

			default {
				float leave_time;
				ask t {
					leave_time <- entry_time + getRoadTravelTime(myself);
				}
				if present_transports.isEmpty() {
					ask t {
						do setLeaveTime(leave_time with_precision 3);
					}
				}

				ask present_transports {
					do add([leave_time, t]);
				}
			}

		}
		
	}

	//action called by a transport when it leaves the road
	action leave (Transport t, float signal_time) {
		switch species(t) {
			match Bike {
				if not has_bike_lane {
					current_capacity <- current_capacity + t.size;
				}

				remove t from: present_bikes;
			}

			match Walk {
				remove t from: present_pedestrians;
			}
			
			match Bus {
				if has_bus_lane{
					ask present_buses {
						do remove;
					}
					if not present_transports.isEmpty() {
						ask getHeadPresentBus() {
							do setLeaveTime(max(myself.getHeadPresentBusLeaveTime(), signal_time + myself.output_flow_capacity) with_precision 3);
						}
					}
				}else{
					current_capacity <- current_capacity + t.size;
					ask present_transports {
						do remove;
					}
					do acceptTransport(signal_time);
					if not present_transports.isEmpty() {
						ask getHeadPresentTransport() {
							do setLeaveTime(max(myself.getHeadPresentTransportLeaveTime(), signal_time + myself.output_flow_capacity) with_precision 3);
						}
					}
				}
			}

			default {
				current_capacity <- current_capacity + t.size;
				ask present_transports {
					do remove;
				}

				do acceptTransport(signal_time);
				if not present_transports.isEmpty() {
					ask getHeadPresentTransport() {
						do setLeaveTime(max(myself.getHeadPresentTransportLeaveTime(), signal_time + myself.output_flow_capacity) with_precision 3);
					}

				}

			}

		}

	}

	float getHeadPresentTransportLeaveTime {
		return float(present_transports.element()[0]);
	}

	Transport getHeadPresentTransport {
		return Transport(present_transports.element()[1]);
	}
	
	float getHeadPresentBusLeaveTime {
		return float(present_buses.element()[0]);
	}

	Bus getHeadPresentBus {
		return Bus(present_buses.element()[1]);
	}

	float getWaitingTimeRequest (int index) {
		return float(waiting_transports.get(index)[0]);
	}

	Transport getWaitingTransport (int index) {
		return Transport(waiting_transports.get(index)[1]);
	}

	bool hasCapacity (float capacity) {
		return current_capacity > capacity;
	}
	
	aspect default {
		geometry geom_display <- (shape + (2.0));
		
		draw geom_display translated_by(trans*2) border: #gray color: rgb(255 * (max_capacity - current_capacity) / max_capacity, 0, 0);
	}

	aspect advanced {
		geometry geom_display <- (shape + (2.0));
		draw geom_display border: #gray color: rgb(255 * (max_capacity - current_capacity) / max_capacity, 0, 0);
		draw "" + type at: location + point([15, -5]) size: 10 color: #black;
		draw "" + length(present_transports.queue) + " transports" at: location + point([15, 15]) size: 10 color: #black;
		draw "" + length(present_bikes) + " bikes" at: location + point([15, 35]) size: 10 color: #black;
		draw "" + length(present_pedestrians) + " walkers" at: location + point([15, 55]) size: 10 color: #black;
	}

	aspect roadTest {
	// Color of the road is determined according to current road occupation
	//rgb color <- rgb(150,255 * (current_capacity / max_capacity),0);
		geometry geom_display <- (shape + (2.5));
		draw geom_display border: #gray color: #black;
		//		draw "" + type + " - " + length(present_transports) + " PCU" at: location + point([15, -5]) size: 10 color: #black;
		float dt <- 0;
		// Display each vehicle in the queue according to their size and colored according to their time_to_leave
		// Vehicles at the top of FIFO are the closet of the end_node.
		float x1 <- start_node.location.x;
		float y1 <- start_node.location.y;
		float x0 <- end_node.location.x;
		float y0 <- end_node.location.y;
		float d <- sqrt(((x1 - x0) * (x1 - x0)) + ((y1 - y0) * (y1 - y0)));
		float distToPoint <- 6;
		float t <- distToPoint / d;
		float xt <- ((1 - t) * x0 + t * x1);
		float yt <- ((1 - t) * y0 + t * y1);
		if(length(present_transports.queue)>0){
		draw box(5, 5, length(present_transports.queue) * 5) at: point([xt, yt, dt]) color: #red rotate: angle_between({x0, y0}, {x1, y0}, {x1, y1});
		dt <- dt + (length(present_transports.queue) * 5) + 1;
		}
		if(length(present_pedestrians)>0){
		draw box(5, 5, length(present_pedestrians) * 5) at: point([xt, yt, dt]) color: #purple rotate: angle_between({x0, y0}, {x1, y0}, {x1, y1});
		dt <- dt + (length(present_pedestrians) * 5) + 1;
		}
		if(length(present_bikes)>0){
		draw box(5, 5, length(present_bikes) * 5) at: point([xt, yt, dt]) color: #green rotate: angle_between({x0, y0}, {x1, y0}, {x1, y1});
		dt <- dt + (length(present_bikes) * 5) + 1;
		}
		distToPoint <- 24;
		t <- distToPoint / d;
		xt <- ((1 - t) * x0 + t * x1);
		yt <- ((1 - t) * y0 + t * y1);
		if(length(waiting_transports.data)>0){
		draw box(5, 5, (length(waiting_transports.data) * 5)) at: point([xt, yt]) color: #yellow rotate: angle_between({x0, y0}, {x1, y0}, {x1, y1});
		}
	}

}



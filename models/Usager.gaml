/**
* Name: Usager
* Based on the internal empty template. 
* Author: chloe
* Tags: 
*/


model Usager

species usager control: simple_bdi{
	float dist_from_work;
	
	predicate have_a_car <- new_predicate("have_a_car");
	predicate have_a_sub <- new_predicate("have_a_sub");
	predicate have_a_bike <- new_predicate("have_a_bike");
	predicate can_walk <- new_predicate("can_walk");
	
	
	aspect default {
	  draw circle(100) color: #yellow border: #black;
	}
	
	
}

/* Insert your model definition here */


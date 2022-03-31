/**
* Name: World
* Based on the internal empty template. 
* Author: Conrad C. Cheriti Y.
* Tags: 
*/
model CogBiais

import "Usager.gaml" 
import "Transport.gaml"


global {
	
		int NbrUsagers <- 100;
		float gasPrice <- 1.0;
		
		// definition of the shape and the size of the map 
		geometry shape <- square(20 #km);
		
		//good weather = 0; bad Weather = 1
		bool weather<- true;
		
		
		predicate bad_weather <- new_predicate("bad_weather");
		predicate good_weather <- new_predicate("bad_weather", false);
		
		
		init {
			create usager number: NbrUsagers;
			create c_car;
			create p_car;
			create bike;
			create foot;
		}
}


/* Insert your model definition here */



experiment name type: gui {

	
	//parameters 
	parameter "Nombre d'usagers :" var: NbrUsagers min: 1 max: 1000;
	parameter "Prix du carburant :" var: gasPrice min: 0.0 max: 4.0;
	parameter "La météo est bonne : si oui, 0 sinon 1 :" var: weather among: [true,false];
	
	
	// Define attributes, actions, a init section and behaviors if necessary
	
	
	output {
	// Define inspectors, browsers and displays here
	
	// inspect one_or_several_agents;
	//

	display map type: opengl {
		
			species usager ;
			species c_car;
			species p_car;
			species bike;
			species foot;
			
		}

	}
}

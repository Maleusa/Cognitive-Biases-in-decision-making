/**
* Name: World
* Based on the internal empty template. 
* Author: Conrad C. Cheriti Y.
* Tags: 
*/
model CogBiais

import "Usager.gaml" 


global {
		int nbrUsagers <- 100;
		float gasPrice <- 1.0;
		
		
		geometry shape <- square(20 #km);
		
		//good weather = 0; bad Weather = 1
		int weather <- 0;
		
		predicate bad_weather <- new_predicate("bad_weather");
		predicate good_weather <- new_predicate("bad_weather", false);
		predicate have_money_for_gas <- new_predicate("have_money");
		

}


/* Insert your model definition here */



experiment name type: gui {

	
	// Define parameters here if necessary
	// parameter "My parameter" category: "My parameters" var: one_global_attribute;
	parameter "Nombre d'usagers :" var: nbrUsagers min: 0 max: 1000;
	parameter "Prix du carburant :" var: gasPrice min: 0.0 max: 4.0;
	parameter "La météo est bonne : si oui, 0 sinon 1 :" var: weather min: 0 max: 1;
	
	
	// Define attributes, actions, a init section and behaviors if necessary
			init {
		create usager number: nbrUsagers;
	}
	
	
	output {
	// Define inspectors, browsers and displays here
	
	// inspect one_or_several_agents;
	//
	display map type: opengl {
		
			species usager ;
			
		}

	}
}
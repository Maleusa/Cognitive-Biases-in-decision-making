/**
* Name: CogBiais
* Based on the internal empty template. 
* Author: yazid
* Tags: 
*/


model CogBiais

/* Transport species, parent of all modes of transportation */
species transport {
	/*Vitesse de déplacement de ce type de transport*/
	int speed;
	float confort;
	
}
/* Personal car species */
species p_car parent: transport {
	init{
		speed<-5;
	}
}

species c_car parent: transport{
	
}

species bike parent: transport {
	
}

species foot parent: transport {
	
}

species 

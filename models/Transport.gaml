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
	aspect default {
	  draw square(1000) color: #red border: #black font: "PC";
	}
}

species c_car parent: transport{
	aspect default {
	  draw square(1000) color: #blue border: #black font: "CC";
	}
	
}

species bike parent: transport {
	aspect default {
	  draw square(1000) color: #pink border: #black font: "B";
	}
}

species foot parent: transport {
	aspect default {
	  draw square(1000) color: #purple border: #black font: "F";
	}
}



/**
* Name: CogBiais
* Based on the internal empty template. 
* Author: yazid
* Tags: 
*/


model CogBiais

/* Insert your model definition here */
species transport {
	int speed;
	float confort;
	
}
species car parent: transport {
	init{
		speed<-5;
	}
}

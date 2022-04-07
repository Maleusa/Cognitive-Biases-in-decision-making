/**
* Name: Metro
* Based on the internal empty template. 
* Author: Lo�c
* Tags: 
*/


model SWITCH

import "PublicTransport.gaml"

species Metro parent: PublicTransport {
	
	string transport_mode <- "metro";
	
	aspect default {
		draw square(1#px) color: #green border: #black depth: 1.0 ;
	}
	
}

/**
* Name: Tram
* Based on the internal empty template. 
* Author: Lo�c
* Tags: 
*/


model SWITCH

import "PublicTransport.gaml"

species Tram parent: PublicTransport {
	
	string transport_mode <- "tram";
	
	aspect default {
		draw square(1#px) color: #green border: #black depth: 1.0 ;
	}
	
}


/***
* Name: Individual
* Author: admin_ptaillandie
* Description: 
* Tags: Tag1, Tag2, TagN
***/
model SWITCH

import "../../Parameters.gaml"

species Building {
	int id;
	string type <- "default";
	string sub_area;
	list<string> types <- [];
	//Number of households in the building
	int nb_households <- 1;
	float size <- shape.perimeter;

	aspect default {
		if (isBuildingDisplayed) {
			switch type {
				match "home" {
					color <- #grey;
				}

				match "work" {
					color <- #red;
				}

				match "school" {
					color <- #cyan;
				}

				match "shop" {
					color <- #gold;
				}

				match "leisure" {
					color <- #magenta;
				}

				default {
					color <- #grey;
				}

			}

			draw shape color: color border: #black;
		}

	}

}

species Outside parent: Building;

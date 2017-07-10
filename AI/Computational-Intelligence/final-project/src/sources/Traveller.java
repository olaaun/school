package sources;

import java.util.ArrayList;
import java.util.List;

public class Traveller {
	public int origin;
	public int destination;
	public List<Integer> orderVisit; //order of visit of the cities
	
	public Traveller(int origin, int destination, List<Integer> orderVisit) {
		this.origin = origin;
		this.destination = destination;
		this.orderVisit = copyList(orderVisit);
	}
	
	//return a copy of the current traveller
	public Traveller copyTraveller() {
		return new Traveller(this.origin, this.destination, this.orderVisit);
	}
	
	//return a copy of the list of order of visit
	public static List<Integer> copyList(List<Integer> liste) {
		List<Integer> response = new ArrayList<Integer>();
		for(Integer city : liste) {
			response.add(city);
		}
		return response;
	}
	
	//return the total cost of the travel of the traveller
	public double totalCostTravel(List<City> cities) {
		double costTravel = cities.get(origin).distance(cities.get(orderVisit.get(0)));
		for(int k = 0; k < orderVisit.size() - 1; k++) {			
			costTravel += cities.get(orderVisit.get(k)).distance(cities.get(orderVisit.get(k+1)));
		}
		costTravel += cities.get(orderVisit.get(orderVisit.size() - 1)).distance(cities.get(destination));
		return costTravel;
	}
	
	//return a string describing the traveller, without access to the position of the cities
	public String toStringWithId(String name) {
		String res;
		res = "Traveller " + name + ": \n";
		res += "	origin - pos " + origin + "\n";
		for(int k = 0; k < orderVisit.size(); k++) {
			res += "		stopover " + k + " - pos " + orderVisit.get(k) + "\n";
		}
		res += "	destination - pos " + destination + "\n";
		return res;
	}

	//return a string describing the traveller, with access to the position of the cities
	public String toStringWithCity(String name, List<City> cities) {
		String res;
		res = "Traveller " + name + ": \n";
		res += "	origin - " + cities.get(origin).toStringCity() + "\n";
		for(int k = 0; k < orderVisit.size(); k++) {
			res += "		stopover " + k + " - " + cities.get(orderVisit.get(k)).toStringCity() + "\n";
		}
		res += "	destination - " + cities.get(destination).toStringCity() + "\n";
		res += "	total travel cost : " + this.totalCostTravel(cities) + "\n";
		return res;
	}
	
	public String toOneLineString(List<City> cities) {
		String order = totalCostTravel(cities) + "   ";
				
		order += cities.get(origin).name + ",";
		
		for (Integer index : orderVisit) {
			order += cities.get(index).name + ",";
		}

		order += cities.get(destination).name;

		return(order);
	}
	
}

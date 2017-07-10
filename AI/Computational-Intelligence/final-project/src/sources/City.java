package sources;

public class City {
	public String name;
	public double lat;
	public double lng;
	
	public City() {
	}
	
	public City(String name, double lat, double lng){
		this.name = name;
		this.lat = lat;
		this.lng = lng;
	}
	
	
	public double distance(City otherCity){
		int R = 6378; 
		//Turn the radius in radians
		double lat_a = Math.toRadians(this.lat);
		double lon_a = Math.toRadians(this.lng);
		double lat_b = Math.toRadians(otherCity.lat);
		double lon_b = Math.toRadians(otherCity.lng);
		
		//calculation of the distance from the city in parameter
		double d = R * (Math.PI/2 - Math.asin( Math.sin(lat_b) * Math.sin(lat_a) + Math.cos(lon_b - lon_a) * Math.cos(lat_b) * Math.cos(lat_a)));
		return d;
	}
	
	public String toStringCity() {
		return "City " + name + " : lat = " + lat + ", lng = " + lng;
	}
	
	@Override
	public boolean equals(Object obj) {
		City other = (City)obj;
		return this.name.equals(other.name);
	}
}
